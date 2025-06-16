from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QMessageBox
) #layout widgets
import os #interaction with system

class ProjectWizard(QWidget): #project wizard class
    def __init__(self, return_callback, back_callback):
        super().__init__()
        self.setWindowTitle("Project Wizard") #window title
        self.setGeometry(400, 250, 500, 300) #size of window

        self.return_callback = return_callback #next window
        self.back_callback = back_callback #back window

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout() #layout storage

        # Base project path
        path_layout = QHBoxLayout() #pathbox horizontal
        path_label = QLabel("Project path:") #label to indentify what user should put in
        self.path_input = QLineEdit() #line edit to add input by typing
        path_browse_btn = QPushButton("📁") #folder search to get the path by searching
        path_browse_btn.clicked.connect(self.browse_base_path) #connect the logic to the path for project
        path_layout.addWidget(path_label) #add to horizontal box
        path_layout.addWidget(self.path_input) #add to horizontal box
        path_layout.addWidget(path_browse_btn) #add to horizontal box
        layout.addLayout(path_layout) #add total horizontal layout to vertical layout

        # Project name
        self.project_name_input = QLineEdit() #project name input by typing
        project_layout = QHBoxLayout() #layout storage for input name
        project_layout.addWidget(QLabel("Project name:")) #add label
        project_layout.addWidget(self.project_name_input) #add line edit
        layout.addLayout(project_layout) #add horizontal layout to the vertical one

        # Config file
        self.config_path_input = QLineEdit() #line edit to put in config file by typing
        config_btn = QPushButton("📄") #search file in folder
        config_btn.clicked.connect(self.browse_config_file) #connect button logic to the path in python

        config_layout = QHBoxLayout() #make layout storage for config file
        config_layout.addWidget(QLabel("Settings config file:")) # add label
        config_layout.addWidget(self.config_path_input) #add line edit
        config_layout.addWidget(config_btn) #add file button
        layout.addLayout(config_layout) #add totaal config horizontal layout to vertical layout

        # Input files
        self.inputs = [] #create input files. 
        for i in range(3): #aantal input files (kan aangepast worden)
            input_line = QLineEdit() #add een line edit for typing
            input_btn = QPushButton("📂") #search a folder (moet file waarschijnlijk worden)
            input_btn.clicked.connect(lambda _, line=input_line: self.browse_input_file(line)) #add button logic to python

            input_layout = QHBoxLayout() #create a horizontal storage for layout input file
            input_layout.addWidget(QLabel(f"Input {i+1}:")) # add label
            input_layout.addWidget(input_line) #add line edit
            input_layout.addWidget(input_btn) #add input file button

            layout.addLayout(input_layout) #add the input line into the vertical layout
            self.inputs.append(input_line) #add the inputfile to the totaal inputs

        # Buttons back and next/return
        btn_layout = QHBoxLayout() # horizontal button storage
        back_btn = QPushButton("Back") #button back
        back_btn.clicked.connect(self.back_callback) #connect the logic to return to the previous window

        return_btn = QPushButton("Return") #button return
        return_btn.clicked.connect(self.return_to_main) #connect the logic to go to the main screen

        btn_layout.addWidget(back_btn) #add back button to the horizontal layout
        btn_layout.addWidget(return_btn) #add return button to the horizontal layout
        layout.addLayout(btn_layout) #add buttons to vertical layout

        self.setLayout(layout) #set layout

    def browse_base_path(self): #function to set project base folder.
        folder = QFileDialog.getExistingDirectory(self, "Select Base Folder for Project") #search folder in system
        if folder: #if folder found/selected
            self.path_input.setText(folder) #set base path

    def browse_config_file(self): #function to find config file
        file, _ = QFileDialog.getOpenFileName(self, "Select Config File", "", "JSON Files (*.json)") #Search config file in system
        if file: #if found/selected
            self.config_path_input.setText(file) #set configuration file path

    def browse_input_file(self, line_edit): #function to create input file path
        file, _ = QFileDialog.getOpenFileName(self, "Select Input File") #search input file path
        if file: #if found/selected
            line_edit.setText(file) #set input file path

    def return_to_main(self): #function to go to main project window.
        project_name = self.project_name_input.text().strip() #set project namen
        project_dir = self.path_input.text().strip() #set project directory
        config_path = self.config_path_input.text().strip() #set config path

        if not project_name or not project_dir or not os.path.isdir(project_dir): # if name or directory is not set correct
            QMessageBox.warning(self, "Input Error", "Please enter a valid project name and path.") #give error
            return

        if not config_path or not os.path.isfile(config_path): #check if config path is set correctly
            QMessageBox.warning(self, "Input Error", "Please select a valid settings config file.") #give error if not
            return

        full_project_path = os.path.join(project_dir, project_name) #join paths to create full path

        # Create folder structure
        try:
            if not os.path.exists(full_project_path): #if full path is not correct
                os.makedirs(full_project_path) #make path
            self.stages = ["Schematics","RTL-designs","Simulations","Layouts"]
            for stage in self.stages: #folder structuur (moet aangepast worden naar schematic/layout die shit door array te maken)
                stage_folder = f"{stage}"  # 'a' to 'e' #create folder
                action_path = os.path.join(full_project_path, stage_folder) #join folder path create the folder
                if stage == "Simulations" or stage == "Layouts":
                    os.makedirs(os.path.join(action_path, "Analog"), exist_ok=True) # create also a analog folder
                    os.makedirs(os.path.join(action_path, "Digital"), exist_ok=True) # create Digital folder
                    os.makedirs(os.path.join(action_path, "Mixed"), exist_ok=True) # create mixed folder
                else:
                    # Just create the base folder for Schematics and RTL-designs
                    os.makedirs(action_path, exist_ok=True)

        except Exception as e: #do check if succesfull
            QMessageBox.critical(self, "Folder Error", f"Could not create folder structure:\n{str(e)}") #error if not
            return

        input_files = [line.text().strip() for line in self.inputs if line.text().strip()] #add the input files
        self.return_callback(full_project_path,project_name, config_path, input_files) #go to mainwindow with the configured files
        self.close() #close window