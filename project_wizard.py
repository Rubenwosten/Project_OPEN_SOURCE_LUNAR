from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
import os

class ProjectWizard(QWidget):
    def __init__(self, return_callback, back_callback):
        super().__init__()
        self.setWindowTitle("Project Wizard")
        self.setGeometry(400, 250, 500, 300)

        self.return_callback = return_callback
        self.back_callback = back_callback

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Base project path
        path_layout = QHBoxLayout()
        path_label = QLabel("Project path:")
        self.path_input = QLineEdit()
        path_browse_btn = QPushButton("📁")
        path_browse_btn.clicked.connect(self.browse_base_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(path_browse_btn)
        layout.addLayout(path_layout)

        # Project name
        self.project_name_input = QLineEdit()
        project_layout = QHBoxLayout()
        project_layout.addWidget(QLabel("Project name:"))
        project_layout.addWidget(self.project_name_input)
        layout.addLayout(project_layout)

        # Config file
        self.config_path_input = QLineEdit()
        config_btn = QPushButton("📄")
        config_btn.clicked.connect(self.browse_config_file)

        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Settings config file:"))
        config_layout.addWidget(self.config_path_input)
        config_layout.addWidget(config_btn)
        layout.addLayout(config_layout)

        # Input files
        self.inputs = []
        for i in range(3):
            input_line = QLineEdit()
            input_btn = QPushButton("📂")
            input_btn.clicked.connect(lambda _, line=input_line: self.browse_input_file(line))

            input_layout = QHBoxLayout()
            input_layout.addWidget(QLabel(f"Input {i+1}:"))
            input_layout.addWidget(input_line)
            input_layout.addWidget(input_btn)

            layout.addLayout(input_layout)
            self.inputs.append(input_line)

        # Buttons
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.back_callback)

        return_btn = QPushButton("Return")
        return_btn.clicked.connect(self.return_to_main)

        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(return_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def browse_base_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Base Folder for Project")
        if folder:
            self.path_input.setText(folder)

    def browse_config_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Config File", "", "JSON Files (*.json)")
        if file:
            self.config_path_input.setText(file)

    def browse_input_file(self, line_edit):
        file, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if file:
            line_edit.setText(file)

    def return_to_main(self):
        project_name = self.project_name_input.text().strip()
        project_dir = self.path_input.text().strip()
        config_path = self.config_path_input.text().strip()

        if not project_name or not project_dir or not os.path.isdir(project_dir):
            QMessageBox.warning(self, "Input Error", "Please enter a valid project name and path.")
            return

        if not config_path or not os.path.isfile(config_path):
            QMessageBox.warning(self, "Input Error", "Please select a valid settings config file.")
            return

        full_project_path = os.path.join(project_dir, project_name)

        # Create folder structure
        try:
            if not os.path.exists(full_project_path):
                os.makedirs(full_project_path)

            for i in range(5):
                action_folder = f"action_{chr(97 + i)}"  # 'a' to 'e'
                action_path = os.path.join(full_project_path, action_folder)
                os.makedirs(os.path.join(action_path, "input"), exist_ok=True)
                os.makedirs(os.path.join(action_path, "output"), exist_ok=True)

        except Exception as e:
            QMessageBox.critical(self, "Folder Error", f"Could not create folder structure:\n{str(e)}")
            return

        input_files = [line.text().strip() for line in self.inputs if line.text().strip()]
        self.return_callback(full_project_path, config_path, input_files)
        self.close()