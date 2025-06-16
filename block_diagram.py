# Import necessary PyQt5 modules for graphics, GUI elements, and core functionality
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QMenu, QAction
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import Qt

import json  # Import the JSON module for reading data
import os    # Import the OS module to check file existence


# Define a custom canvas for displaying blocks using QGraphicsView
class BlockCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()  # Initialize the base QGraphicsView

        # Create a graphics scene that will hold the block items
        self.scene = QGraphicsScene()

        # Attach the scene to the view
        self.setScene(self.scene)

        # Enable antialiasing for smoother graphics
        self.setRenderHint(QPainter.Antialiasing)

        # Set the visible area of the scene to 1000x800 pixels
        self.setSceneRect(0, 0, 1000, 800)

        # Keep track of added blocks (each entry holds data, rect item, and text item)
        self.blocks = []

    # Add a new block to the scene
    def add_block(self, block):
        # Extract position (x, y) and size (width, height) from the block dictionary
        x, y = block['position']
        w, h = block['size']

        # Choose color based on block type: blue for analog, green for digital
        color = QColor("lightblue") if block['type'] == "analog" else QColor("lightgreen")

        # Create a rectangle item to visually represent the block
        rect_item = QGraphicsRectItem(x, y, w, h)

        # Fill the rectangle with the selected color
        rect_item.setBrush(QBrush(color))

        # Allow the rectangle to be moved with the mouse
        rect_item.setFlag(QGraphicsRectItem.ItemIsMovable)

        # Allow the rectangle to be selected with the mouse
        rect_item.setFlag(QGraphicsRectItem.ItemIsSelectable)

        # Store the block name as metadata in the rectangle (can be retrieved later)
        rect_item.setData(0, block['name'])

        # Create a text label item to display the block's name
        text_item = QGraphicsTextItem(block['name'])

        # Set the text color to black
        text_item.setDefaultTextColor(Qt.black)

        # Position the text near the top-left corner of the rectangle
        text_item.setPos(x + 5, y + 5)

        # Add both rectangle and label to the graphics scene
        self.scene.addItem(rect_item)
        self.scene.addItem(text_item)

        # Keep a reference to the block's data and graphics items
        self.blocks.append((block, rect_item, text_item))

    # Override the context menu event to show a right-click menu on blocks
    def contextMenuEvent(self, event):
        # Check if the user right-clicked on a graphics rectangle item
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsRectItem):
            # Create a context menu
            menu = QMenu(self)

            # Add options to the context menu
            add_pin_action = QAction("Add Pin", self)
            remove_block_action = QAction("Remove Block", self)
            menu.addAction(add_pin_action)
            menu.addAction(remove_block_action)

            # Show the menu at the cursor position and wait for user to choose an action
            action = menu.exec_(event.globalPos())

            # If the user selected "Remove Block", remove it from the scene
            if action == remove_block_action:
                self.scene.removeItem(item)
                # (Optional) you might also want to remove it from self.blocks here

    # Load block data from a JSON file and add them to the canvas
    def load_blocks_from_file(self, json_path="blocks.json"):
       
        # If the JSON file exists at the given path
        if os.path.exists(json_path):
            # Open and read the JSON file
            with open(json_path, 'r') as f:
                blocks = json.load(f)

                # Add each loaded block to the canvas
                for block in blocks:
                    self.add_block(block)
    def save_blocks_to_file(self, json_path="blocks.json"):
        updated_blocks = []

        for block, rect_item, text_item in self.blocks:
            # Get the updated position from the scene
            pos = rect_item.scenePos()
            block['position'] = [int(pos.x()), int(pos.y())]

            updated_blocks.append(block)

        # Write updated block data to file
        with open(json_path, 'w') as f:
            json.dump(updated_blocks, f, indent=4)

        print(f"Saved {len(updated_blocks)} blocks to {json_path}")

    