from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLineEdit, QFileSystemModel, QTreeView,
    QSplitter, QMenuBar, QAction, QStatusBar, QPushButton, QLabel, QFileDialog, QDialog
)
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QPixmap
import os
from automate_gds import AUTOMATE
import shutil 
from add_block_dialog import AddBlockDialog
import json
class MainProjectWindow(QMainWindow):
    def __init__(self, project_path, project_name, shared):
        super().__init__()
        self.setWindowTitle("Analog IC Toolchain - Project View")
        self.setGeometry(200, 100, 1200, 800)
        self.auto = AUTOMATE(project_name, project_path, shared)
        self.shared = shared
        self.project_path = project_path
        self.project_name = project_name

        central_widget = QWidget()
        central_layout = QVBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_blocks)
        central_layout.addWidget(save_button)

        create_button = QPushButton("Create")
        create_button.clicked.connect(self.create_gds)
        central_layout.addWidget(create_button)

        splitter = QSplitter(Qt.Horizontal)

        # File tree
        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(project_path)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(project_path))
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.doubleClicked.connect(self.file_double_clicked)
        splitter.addWidget(self.tree_view)

        # Terminal output area
        self.output_terminal = QPlainTextEdit()
        self.output_terminal.setReadOnly(True)
        splitter.addWidget(self.output_terminal)
        splitter.setStretchFactor(1, 3)

        # Command input
        self.input_terminal = QLineEdit()
        self.input_terminal.setPlaceholderText("Input terminal – type a command and press Enter...")
        self.input_terminal.returnPressed.connect(self.handle_input)

        central_layout.addWidget(splitter)
        central_layout.addWidget(self.input_terminal)

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self._create_menu_bar()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("Open", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self))

        settings_menu = menu_bar.addMenu("Settings")
        settings_menu.addAction(QAction("Preferences", self))

        tools_menu = menu_bar.addMenu("blocks")
        add_block_action = QAction("Add Block", self)
        add_block_action.triggered.connect(self.addblock)
        tools_menu.addAction(add_block_action)

        run_menu = menu_bar.addMenu("Run")
        run_menu.addAction(QAction("Start Flow", self))

    def handle_input(self):
        command = self.input_terminal.text().strip()
        if command:
            self.output_terminal.appendPlainText(f"> {command}")
            # Here, you could parse and handle basic shell-like commands
            self.input_terminal.clear()

    def save_blocks(self):
        # placeholder for save, if diagram view removed
        self.output_terminal.appendPlainText("[INFO] Save button clicked — implement logic here.")

    def create_gds(self):

        # placeholder for block processing
        self.output_terminal.appendPlainText("[INFO] Creating GDS files...")
        json_path = os.path.join(self.project_path, "blocks.json")
        with open(json_path, "r") as f:
            blocks = json.load(f)
        for block in blocks:
            print(block)
            self.auto.automation(block)

    def file_double_clicked(self, index):
        path = self.model.filePath(index)
        if path.lower().endswith(".png"):
            self.output_terminal.appendPlainText(f"[PREVIEW] Opening PNG: {path}")
            self.preview_png(path)
        else:
            self.output_terminal.appendPlainText(f"[INFO] Opened file: {path}")

    def addblock(self):
        dialog = AddBlockDialog(self.project_path, self)
        if dialog.exec_() == QDialog.Accepted:
            self.output_terminal.appendPlainText("[INFO] Block dialog closed. Processing blocks...")

            json_path = os.path.join(self.project_path, "blocks.json")

            # Step 1: Read the JSON file
            if not os.path.exists(json_path):
                self.output_terminal.appendPlainText("[ERROR] blocks.json not found.")
                return

            with open(json_path, "r") as f:
                blocks = json.load(f)

            updated_blocks = []

            # Step 2: Loop over all blocks and place files
            for block in blocks:
                block_name = block.get("name", "unnamed")
                block_type = block.get("type", "unknown")

                # Skip if name/type missing
                if block_type not in ["analog", "digital", "mixed"]:
                    self.output_terminal.appendPlainText(f"[SKIPPED] Block {block_name} has unknown type.")
                    updated_blocks.append(block)
                    continue

                # Target folder
                target_dir = os.path.join(self.project_path, block_type, block_name)
                os.makedirs(target_dir, exist_ok=True)

                # File fields to process
                file_fields = ["beheviour", "Constraint", "symbol", "sim","config", "gds_path"]
                for field in file_fields:
                    file_path = block.get(field, "")
                    print(file_path)
                    if file_path and os.path.exists(file_path):
                        filename = os.path.basename(file_path)
                        dest_dir = os.path.join(target_dir,field)
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_path = os.path.join(dest_dir, filename)
                        try:
                            shutil.copy(file_path, dest_path)
                            block[field] = dest_path  # Update path in block
                        except Exception as e:
                            self.output_terminal.appendPlainText(f"[ERROR] Copying {file_path}: {e}")
                    else:
                        self.output_terminal.appendPlainText(f"[WARNING] {field} missing or invalid for {block_name}")

                updated_blocks.append(block)
                self.output_terminal.appendPlainText(f"[SUCCESS] Block '{block_name}' moved to '{block_type}/'")

            # Step 3: Save updated JSON
            with open(json_path, "w") as f:
                json.dump(updated_blocks, f, indent=4)

            self.output_terminal.appendPlainText("[DONE] All blocks processed and paths updated.")
        else:
            self.output_terminal.appendPlainText("[CANCELLED] Block addition cancelled.")

    def preview_png(self, path):
        dialog = QWidget()
        dialog.setWindowTitle(os.path.basename(path))
        layout = QVBoxLayout()
        label = QLabel()
        pixmap = QPixmap(path)
        label.setPixmap(pixmap.scaledToWidth(600, Qt.SmoothTransformation))
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.setGeometry(300, 200, 650, 500)
        dialog.show()
        # Keep a reference so it doesn’t get garbage collected
        self.png_dialog = dialog