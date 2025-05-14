import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QAction
)
from settings_window import SettingsWindow
from project_wizard import ProjectWizard
from main_project_window import MainProjectWindow
import os
import json

CONFIG_FILE = "config.json"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analog IC Toolchain")
        self.setGeometry(300, 200, 500, 400)

        # Settings state
        self.design_type = "-----"
        self.automation_level = "-----"
        self.load_config() #load configuration file.
        self.init_ui()

    def init_ui(self):
        # Create central widget (main screen)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title = QLabel("Analog IC Toolchain")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Buttons
        new_btn = QPushButton("New Project")
        new_btn.clicked.connect(self.new_project)

        open_btn = QPushButton("Open Project")
        open_btn.clicked.connect(self.open_project)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.open_settings)

        for btn in [new_btn, open_btn, settings_btn]:
            btn.setFixedHeight(40)
            layout.addWidget(btn)

        central_widget.setLayout(layout)

        # Set up menu bar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)

        open_action = QAction("Open Project", self)
        open_action.triggered.connect(self.open_project)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        for action in [new_action, open_action, settings_action, exit_action]:
            file_menu.addAction(action)

        # Optional: Add a status bar (future use)
        self.statusBar().showMessage("Ready")

    def new_project(self):
        if self.design_type == "-----":
            QMessageBox.warning(self, "Missing Settings", "Please select a design type in Settings before creating a new project.")
        elif self.automation_level == "-----":
            QMessageBox.warning(self, "Missing Settings", "Please select an automation level in Settings before creating a new project.")
        else:
            self.project_wizard = ProjectWizard(
                return_callback=self.start_project,
                back_callback=self.project_wizard_back
            )
            self.project_wizard.show()
    def project_wizard_back(self):
        self.project_wizard.close()

    def start_project(self, project_name, config_path, input_files):
        self.project_wizard.close()
        self.main_project_window = MainProjectWindow(project_name)
        self.main_project_window.show()
        # Here, you could initialize folders, load config, etc.

    def open_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Project Folder")
        if folder:
            QMessageBox.information(self, "Open Project", f"Opened: {folder}")
            self.statusBar().showMessage(f"Opened: {folder}")

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def save_config(self):
        config = {
        "design_type": self.design_type,
        "automation_level": self.automation_level
    }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.design_type = config.get("design_type", "-----")
                self.automation_level = config.get("automation_level", "-----")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())