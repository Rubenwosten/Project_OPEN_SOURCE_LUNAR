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

def load_blocks(path): # function to load the json file
    if os.path.exists(path): #zoek het pad
        with open(path, 'r') as f: #open pad
            return json.load(f) #load the blocks
    return [] #if not then is empty

def save_blocks(blocks, path): # save blocks function
    with open(path, 'w') as f: #open json file
        json.dump(blocks, f, indent=4) #update json file

class AddBlockDialog(QDialog):
    def __init__(self, project_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Block") #block window
        self.setMinimumWidth(400) #window width
        self.block_data = None #data nog niet
        self.init_ui() #naar ui code
        self.project_path = project_path
        self.json_path = os.path.join(self.project_path, "blocks.json")  # Use project-specific pat

    def init_ui(self):
        # Main vertical layout for the dialog
        layout = QVBoxLayout()

        # Form layout to organize labels and input fields in rows
        form_layout = QFormLayout()

        # Input field for block name
        self.name_edit = QLineEdit()

        self.behevior = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_beheviour)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        beh_layout = QHBoxLayout()
        beh_layout.addWidget(self.behevior)
        beh_layout.addWidget(self.browse_btn)

        self.constraint = QLineEdit()
        self.browse_btn_c = QPushButton("Browse")
        self.browse_btn_c.clicked.connect(self.browse_constraint)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        con_layout = QHBoxLayout()
        con_layout.addWidget(self.constraint)
        con_layout.addWidget(self.browse_btn_c)
        
        self.sim_file = QLineEdit()
        self.browse_btn_s = QPushButton("Browse")
        self.browse_btn_s.clicked.connect(self.browse_sim)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        sim_layout = QHBoxLayout()
        sim_layout.addWidget(self.sim_file)
        sim_layout.addWidget(self.browse_btn_s)

        self.sym = QLineEdit()
        self.browse_btn_sy = QPushButton("Browse")
        self.browse_btn_sy.clicked.connect(self.browse_sym)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        sym_layout = QHBoxLayout()
        sym_layout.addWidget(self.sym)
        sym_layout.addWidget(self.browse_btn_sy)

        self.config = QLineEdit()
        self.browse_btn_co = QPushButton("Browse")
        self.browse_btn_co.clicked.connect(self.browse_co)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        co_layout = QHBoxLayout()
        co_layout.addWidget(self.config)
        co_layout.addWidget(self.browse_btn_co)
        # Input field for GDS file path and a button to browse files
        self.gds = QLineEdit()
        self.browse_btn_l = QPushButton("Browse")
        self.browse_btn_l.clicked.connect(self.browse_gds)  # Connect the browse button to file dialog

        # Horizontal layout to combine the GDS path input and browse button
        gds_layout = QHBoxLayout()
        gds_layout.addWidget(self.gds)
        gds_layout.addWidget(self.browse_btn_l)


        # Dropdown to select block type: "analog" or "digital"
        self.type_combo = QComboBox()
        self.type_combo.addItems(["analog", "digital","mixed"])

        # Add all labeled fields to the form layout
        form_layout.addRow("Block Name:", self.name_edit)
        form_layout.addRow("Schematic Path:", beh_layout)
        form_layout.addRow("Constraint file:", con_layout)
        form_layout.addRow("Simulation file:", sim_layout)
        form_layout.addRow("Symbol file:", sym_layout)
        form_layout.addRow("config file:", co_layout)         
        form_layout.addRow("GDS Path:", gds_layout)
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
            self.gds.setText(file)  # Display the selected file path in the input field
    def browse_sym(self):
        # Open a file dialog to let the user choose a GDS file
        file, _ = QFileDialog.getOpenFileName(self, "Select symbol File")
        if file:
            self.sym.setText(file)  # Display the selected file path in the input field
    def browse_sim(self):
        # Open a file dialog to let the user choose a GDS file
        file, _ = QFileDialog.getOpenFileName(self, "Select simulation File")
        if file:
            self.sim_file.setText(file)  # Display the selected file path in the input field
    def browse_beheviour(self):
        # Open a file dialog to let the user choose a GDS file
        file, _ = QFileDialog.getOpenFileName(self, "Select beheviour File")
        if file:
            self.behevior.setText(file)  # Display the selected file path in the input field
    def browse_constraint(self):
        # Open a file dialog to let the user choose a GDS file
        file, _ = QFileDialog.getOpenFileName(self, "Select constraint File")
        if file:
            self.constraint.setText(file)  # Display the selected file path in the input field
    def browse_co(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select configuration File")
        if file:
            self.config.setText(file)
    def accept_data(self):
        try:
            # Retrieve values from input fields
            name = self.name_edit.text() #get name
            beheviour_path = self.behevior.text() #get schematic path
            Constraint = self.constraint.text() #get schematic path
            sym_path = self.sym.text() #get schematic path
            sim = self.sim_file.text() #get schematic path
            confi = self.config.text()
            gds_path = self.gds.text() #get gds path
            block_type = self.type_combo.currentText() #get type (analog/digital block)

            # Store the data in a dictionary (dictornary kan worden uitbereid. Zowel hier in deze code toevoegen en dan ook in datastructure.py)
            self.block_data = {
                "name": name,
                "beheviour": beheviour_path,
                "Constraint": Constraint,
                "symbol":sym_path,
                "config": confi,
                "sim" : sim,
                "gds_path": gds_path,
                "type": block_type
            }

            # Load existing blocks from file, append the new one, and save
            blocks = load_blocks(self.json_path)
            blocks.append(self.block_data)
            save_blocks(blocks, self.json_path)

            self.accept()  # Close the dialog with success
        except ValueError:
            pass  # In production, show an error message if conversion to int fails