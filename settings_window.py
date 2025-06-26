from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QFileDialog

class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Reference to the main window
        self.setWindowTitle("Settings")
        self.setGeometry(400, 250, 300, 150)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Design type dropdown
        self.combo = QComboBox()
        self.combo.addItems(["-----", "Mixed Signal", "Analog Signal", "Digital Signal"])
        self.combo.setCurrentText(self.parent.design_type)
        self.combo.currentIndexChanged.connect(self.update_setting)

        # Automation level dropdown
        self.automation_combo = QComboBox()
        self.automation_combo.addItems(["-----", "Fully", "Semi", "Complete user controll"])
        self.automation_combo.setCurrentText(self.parent.automation_level)
        self.automation_combo.currentIndexChanged.connect(self.update_setting)

        # Shared folder path input
        self.input_line = QLineEdit()
        self.input_line.setText(self.parent.shared_path)  # Load current setting
        input_btn = QPushButton("📂")
        input_btn.clicked.connect(self.browse_input_folder)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Shared folder:"))
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(input_btn)

        # Add widgets to layout
        layout.addWidget(QLabel("Select design type:"))
        layout.addWidget(self.combo)
        layout.addWidget(QLabel("Select automation level:"))
        layout.addWidget(self.automation_combo)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def browse_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Shared Folder")
        if folder:
            self.input_line.setText(folder)
            self.update_setting()  # Immediately update setting when folder is chosen

    def update_setting(self):
        self.parent.design_type = self.combo.currentText()
        self.parent.automation_level = self.automation_combo.currentText()
        self.parent.shared_path = self.input_line.text()
        self.parent.save_config()