import json
import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction, QInputDialog, QDialog

from add_block_dialog import save_blocks, AddBlockDialog  # Import the function you mentioned


class BlockDiagramView(QGraphicsView):
    

    def __init__(self, project_path, parent=None):
        super().__init__(parent) #add this to the parent window
        self.scene = QGraphicsScene() #create a canvas to create block chip
        self.setScene(self.scene) #set canvas
        self.setRenderHint(QPainter.Antialiasing) #Enables antialiasing, which smooths out jagged edges of graphics
        self.setBackgroundBrush(QBrush(Qt.white)) #Sets the background color or texture of the view (aanpassen naar grid can hiervoor gebruikt worden)
        self.project_path = project_path
        self.blocks = []  # Keep track of blocks added (dict + rect + label)
        self.json_path = os.path.join(self.project_path, "blocks.json")  # Use project-specific pat

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
        label = QGraphicsTextItem(name, rect)
        label.setPos(10, 10)  # Now relative to the top-left of the rect

        # Add the rectangle to the graphics scene so it appears in the view
        self.scene.addItem(rect)


        # Add the text label to the graphics scene
        self.scene.addItem(label)

        # Keep a reference to the block's data, rectangle, and label for later use (e.g., selection, updates)
        self.blocks.append((block_data, rect, label))

    def load_blocks_from_file(self): #function to load the blocks out of the saved json file
        
        if os.path.exists(self.json_path): #if the json file exist 
            with open(self.json_path, 'r') as f: #open json file
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
            # Convert click position from view to scene coordinates
            scene_pos = self.mapToScene(event.pos())

            # Launch the custom dialog
            dialog = AddBlockDialog(self.project_path)  # You must provide the project path here
            dialog.x_edit.setText(str(int(scene_pos.x())))
            dialog.y_edit.setText(str(int(scene_pos.y())))
            dialog.w_edit.setText("120")  # default width
            dialog.h_edit.setText("60")   # default height

            if dialog.exec_() == QDialog.Accepted:
                block_data = dialog.block_data
                self.add_block(block_data)
    def save_blocks_to_file(self):
        # Convert current blocks into dictionaries
        block_dicts = [block for block, _, _ in self.blocks]
        save_blocks(block_dicts, self.json_path)
    def block_return(self):
            
        updated_blocks = []

        for block_data, rect_item, _ in self.blocks:
            # Get current position of the rectangle item
            pos = rect_item.scenePos()

            # Copy original data to avoid modifying original block_data
            updated_block = dict(block_data)
            updated_block['position'] = [int(pos.x()), int(pos.y())]

            updated_blocks.append(updated_block)

        return updated_blocks