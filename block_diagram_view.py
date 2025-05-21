import json
import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction, QInputDialog

class BlockDiagramView(QGraphicsView):
    JSON_PATH = "blocks.json"  # You can change this path

    def __init__(self, parent=None):
        super().__init__(parent) #add this to the parent window
        self.scene = QGraphicsScene() #create a canvas to create block chip
        self.setScene(self.scene) #set canvas
        self.setRenderHint(QPainter.Antialiasing) #Enables antialiasing, which smooths out jagged edges of graphics
        self.setBackgroundBrush(QBrush(Qt.white)) #Sets the background color or texture of the view (aanpassen naar grid can hiervoor gebruikt worden)

        self.blocks = []  # Keep track of blocks added (dict + rect + label)

        # Load blocks from JSON on startup
        self.load_blocks_from_file()

    def add_block(self, block_data): #function to add blocks
        """
        block_data: dict with keys: name, gds_path (optional), position [x,y], size [w,h], type ("analog"/"digital")
        """
       # Get the (x, y) position of the block from block_data, defaulting to [0, 0] if not specified
        x, y = block_data.get('position', [0, 0])

        # Get the (width, height) size of the block, defaulting to [120, 60] if not provided
        w, h = block_data.get('size', [120, 60])

        # Get the type of block ('analog' or 'digital'), defaulting to 'analog' if not specified
        block_type = block_data.get('type', 'analog')

        # Get the name of the block, defaulting to 'Unnamed' if not specified
        name = block_data.get('name', 'Unnamed')

        # Set the block color based on its type: light blue for analog, light green for digital
        color = QColor("#c0d9ff") if block_type == "analog" else QColor("#c0ffc0")

        # Create a rectangular graphics item representing the block, positioned at (x, y) with size (w, h)
        rect = QGraphicsRectItem(x, y, w, h)

        # Fill the rectangle with the chosen color
        rect.setBrush(QBrush(color))

        # Make the rectangle movable with the mouse
        rect.setFlag(QGraphicsRectItem.ItemIsMovable)

        # Make the rectangle selectable with the mouse
        rect.setFlag(QGraphicsRectItem.ItemIsSelectable)

        # Create a text label item with the block's name
        label = QGraphicsTextItem(name)

        # Position the label slightly inside the rectangle, offset by 10 pixels
        label.setPos(x + 10, y + 10)

        # Add the rectangle to the graphics scene so it appears in the view
        self.scene.addItem(rect)

        # Add the text label to the graphics scene
        self.scene.addItem(label)

        # Keep a reference to the block's data, rectangle, and label for later use (e.g., selection, updates)
        self.blocks.append((block_data, rect, label))

    def load_blocks_from_file(self): #function to load the blocks out of the saved json file
        if os.path.exists(self.JSON_PATH): #if the json file exist 
            with open(self.JSON_PATH, 'r') as f: #open json file
                blocks = json.load(f) #load the blocks out of the json file
                for block in blocks: #loop trough blocks
                    self.add_block(block) #add the blocks at the canvas

    def contextMenuEvent(self, event): #function for the block ajustment
        menu = QMenu(self) #add a menu

        add_block_action = QAction("Add Block Here", self) #add block function for menu
        menu.addAction(add_block_action) #add block function to menu
        # Execute the context menu at the mouse cursor's global screen position
        action = menu.exec_(event.globalPos())
        # Check if the selected action is "Add Block"
        if action == add_block_action:
            # Map the click position from view (widget) coordinates to scene coordinates
            scene_pos = self.mapToScene(event.pos())

            # Prompt the user to enter a block name using a simple input dialog
            name, ok = QInputDialog.getText(self, "Block Name", "Enter block name:")

            # If the user clicked OK and entered a non-empty name
            if ok and name:
                # Create a dictionary representing the block's data
                block_data = {
                    "name": name,  # User-defined block name
                    "gds_path": "",  # Placeholder for GDS path, can be updated later
                    "position": [int(scene_pos.x()), int(scene_pos.y())],  # Click position in scene coords
                    "size": [120, 60],  # Default block size
                    "type": "analog"  # Default block type; could extend to ask the user
                }

                # Add the new block to the scene using the provided data
                self.add_block(block_data)

                # Save the updated list of blocks to file immediately
                self.save_blocks_to_file()