import json # to read and write json file where block layout is saved
import os # to use the system
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QFileDialog, QComboBox,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
    QMenu, QAction
) #layout fucntions
from PyQt5.QtGui import QBrush, QColor #extra layout functions
from PyQt5.QtCore import Qt, QRectF #more layout functions

BLOCK_JSON_PATH = "blocks.json" #create the file for block layout

def load_blocks(): # function to load the json file
    if os.path.exists(BLOCK_JSON_PATH): #zoek het pad
        with open(BLOCK_JSON_PATH, 'r') as f: #open pad
            return json.load(f) #load the blocks
    return [] #if not then is empty

def save_blocks(blocks): # save blocks function
    with open(BLOCK_JSON_PATH, 'w') as f: #open json file
        json.dump(blocks, f, indent=4) #update json file

class AddBlockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Block") #block window
        self.setMinimumWidth(400) #window width
        self.block_data = None #data nog niet
        self.init_ui() #naar ui code

    def init_ui(self):
        # Main vertical layout for the dialog
        layout = QVBoxLayout()

        # Form layout to organize labels and input fields in rows
        form_layout = QFormLayout()

        # Input field for block name
        self.name_edit = QLineEdit()

        # Input field for GDS file path and a button to browse files
        self.gds_path_edit = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_gds)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        gds_layout = QHBoxLayout()
        gds_layout.addWidget(self.gds_path_edit)
        gds_layout.addWidget(self.browse_btn)

        # Input fields for position (x, y) and size (width, height)
        self.x_edit = QLineEdit()
        self.y_edit = QLineEdit()
        self.w_edit = QLineEdit()
        self.h_edit = QLineEdit()

        # Dropdown to select block type: "analog" or "digital"
        self.type_combo = QComboBox()
        self.type_combo.addItems(["analog", "digital"])

        # Add all labeled fields to the form layout
        form_layout.addRow("Block Name:", self.name_edit)
        form_layout.addRow("GDS Path:", gds_layout)
        form_layout.addRow("Position X:", self.x_edit)
        form_layout.addRow("Position Y:", self.y_edit)
        form_layout.addRow("Width:", self.w_edit)
        form_layout.addRow("Height:", self.h_edit)
        form_layout.addRow("Type:", self.type_combo)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Create OK and Cancel buttons with horizontal layout
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept_data)  # Process and save data on OK
        cancel_btn.clicked.connect(self.reject)   # Close dialog without saving on Cancel
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Set the final layout for the dialog
        self.setLayout(layout)

    def browse_gds(self):
        # Open a file dialog to let the user choose a GDS file
        file, _ = QFileDialog.getOpenFileName(self, "Select GDS File", "", "GDS Files (*.gds);;All Files (*)")
        if file:
            self.gds_path_edit.setText(file)  # Display the selected file path in the input field

    def accept_data(self):
        try:
            # Retrieve values from input fields
            name = self.name_edit.text() #get name
            gds_path = self.gds_path_edit.text() #get gds path
            x = int(self.x_edit.text()) #get x coordinaat
            y = int(self.y_edit.text()) #get y coordinaat
            w = int(self.w_edit.text()) #get width
            h = int(self.h_edit.text()) #get heigth
            block_type = self.type_combo.currentText() #get type (analog/digital block)

            # Store the data in a dictionary (dictornary kan worden uitbereid. Zowel hier in deze code toevoegen en dan ook in datastructure.py)
            self.block_data = {
                "name": name,
                "gds_path": gds_path,
                "position": [x, y],
                "size": [w, h],
                "type": block_type
            }

            # Load existing blocks from file, append the new one, and save
            blocks = load_blocks()
            blocks.append(self.block_data)
            save_blocks(blocks)

            self.accept()  # Close the dialog with success
        except ValueError:
            pass  # In production, show an error message if conversion to int fails