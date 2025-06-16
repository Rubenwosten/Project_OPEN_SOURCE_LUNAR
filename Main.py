import sys #module to controll command terminal and also close aplications
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QAction
) #layout widgets
from settings_window import SettingsWindow #settings file
from project_wizard import ProjectWizard #project maak file
from main_project_window import MainProjectWindow #main window om project te bewerken file
import os #om met file systeem om te gaan
import json #write and read of json files.

CONFIG_FILE = "config.json" #configuration file


class MainWindow(QMainWindow): #main class
    def __init__(self): #altijd beginnen met een __init__ om self te configuren en eventuele variable overte zetten
        super().__init__()

        self.setWindowTitle("Analog IC Toolchain") #title of window
        self.setGeometry(300, 200, 500, 400) #grootte window

        # Settings state
        self.design_type = "-----" #bij begin als er nog nooit gewerkt is design type van ic is niks
        self.automation_level = "-----" #bij begin als er nog nooit gewerkt is hoeveelheid automatie type is niks
        self.load_config() #load configuration file.
        self.init_ui() #load ui functie bij intizalizatie

    def init_ui(self):
        # Create central widget (main screen)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout() #layout opslag van main screen

        title = QLabel("DAMs IC Toolchain") #title of the main screen
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;") #text style of title
        layout.addWidget(title) #voeg title toe aan layout boven aan.

        # Buttons
        new_btn = QPushButton("New Project") #create button for new project
        new_btn.clicked.connect(self.new_project) #connect button for new project to function

        open_btn = QPushButton("Open Project") #create button for open project
        open_btn.clicked.connect(self.open_project) #connect button to the function

        settings_btn = QPushButton("Settings") #create button for settings menu
        settings_btn.clicked.connect(self.open_settings) #connect button to the open_settings window

        for btn in [new_btn, open_btn, settings_btn]: #loop voor de buttons in de layout te maken
            btn.setFixedHeight(40) #allemaal zelfde grootte
            layout.addWidget(btn) #voeg ze toe onder elkaar in de layout

        central_widget.setLayout(layout) #zet de layout op main screen

        # Set up menu bar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File") #file menu om files te open en beginnen (moet waarschijnlijk uitgebreid worden)

        new_action = QAction("New Project", self) # new project knop maken onder file menu
        new_action.triggered.connect(self.new_project) #connect de logic aan de button

        open_action = QAction("Open Project", self) #open project knop onder file menu
        open_action.triggered.connect(self.open_project) #connect de logic aan de button

        settings_action = QAction("Settings", self) # settings button #misschien hele nieuwe menu.
        settings_action.triggered.connect(self.open_settings) #logic

        exit_action = QAction("Exit", self) #close project button
        exit_action.triggered.connect(self.close) #connect the logic with the button

        for action in [new_action, open_action, settings_action, exit_action]: #connect the actions to the menu
            file_menu.addAction(action) #add each action to the file menu which is now a dropdown menu

        # Optional: Add a status bar (future use)
        self.statusBar().showMessage("Ready")

    def new_project(self): #new project logic 
        ## first configure the tool. Do checks if done (uitbereiden)
        if self.design_type == "-----": #to create new project ic design type needs to be selected
            QMessageBox.warning(self, "Missing Settings", "Please select a design type in Settings before creating a new project.") #warning box met uitleg want dat is handig
        elif self.automation_level == "-----": #configure automation level first.
            QMessageBox.warning(self, "Missing Settings", "Please select an automation level in Settings before creating a new project.") #warning box met uitleg.
        else: #checks gedaan dan naar project wizard scherm om een project te maken
            self.project_wizard = ProjectWizard(
                return_callback=self.start_project,
                back_callback=self.project_wizard_back
            ) #activate code to load screen
            self.project_wizard.show() #show project wizard screen
    def project_wizard_back(self): #functie om scherm te sluiten mocht het project niet gemaakt te worden.
        self.project_wizard.close() #sluit scherm

    def start_project(self, project_path, project_name, config_path, input_files): # Start functie als het project gecreeerd is
        self.project_wizard.close() #close setup screen
        self.main_project_window = MainProjectWindow(project_path, project_name) #activate main project window code
        self.main_project_window.show() # show window


    def open_project(self): #open project logic
        folder = QFileDialog.getExistingDirectory(self, "Open Project Folder") #choose project folder to open in files on 
        projectnaam = os.path.basename(folder)

        if folder: # if a folder is choosen open main window
            self.main_project_window = MainProjectWindow(folder, projectnaam) #activate main window code
            self.main_project_window.show() #show main window

    def open_settings(self): #settings logic
        self.settings_window = SettingsWindow(self) #activate settings code
        self.settings_window.show() #show settings window

    def save_config(self): # save function to update the json file
        config = {
        "design_type": self.design_type,
        "automation_level": self.automation_level
    } #configurations (uitbereiden)
        with open(CONFIG_FILE, "w") as f: #open config file
            json.dump(config, f, indent=4) #update config file 

    def load_config(self): #load config file function to load the config file while starting the program
        if os.path.exists(CONFIG_FILE): #if exist so after first use
            with open(CONFIG_FILE, "r") as f: #open file
                config = json.load(f) #save file in python variable
                self.design_type = config.get("design_type", "-----") #load configuration value of design type
                self.automation_level = config.get("automation_level", "-----") #load configuration value of automation level

if __name__ == "__main__": #start code
    app = QApplication(sys.argv) #start app
    window = MainWindow() #main window function
    window.show() #show the start window
    sys.exit(app.exec_()) #close function to close app on system.