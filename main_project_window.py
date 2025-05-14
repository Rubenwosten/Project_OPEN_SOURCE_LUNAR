from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLineEdit, QFileSystemModel, QTreeView,
    QSplitter, QMenuBar, QAction, QStatusBar
)
from PyQt5.QtCore import Qt, QDir


class MainProjectWindow(QMainWindow):
    def __init__(self, project_path):
        super().__init__()
        self.setWindowTitle("Analog IC Toolchain - Project View")
        self.setGeometry(200, 100, 1200, 800)  # Wider, taller window

        self.project_path = project_path

        # === Central layout ===
        central_widget = QWidget()
        central_layout = QVBoxLayout()

        # === Splitter to divide folder view and main output ===
        splitter = QSplitter(Qt.Horizontal)

        # === Folder view ===
        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(project_path)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(project_path))
        self.tree_view.setColumnWidth(0, 250)

        splitter.addWidget(self.tree_view)

        # === Main terminal (output) ===
        self.output_terminal = QPlainTextEdit()
        self.output_terminal.setReadOnly(True)
        self.output_terminal.setPlaceholderText("Output terminal – results, logs, status...")
        splitter.addWidget(self.output_terminal)

        splitter.setStretchFactor(1, 3)  # Main terminal gets more space

        # === Input terminal ===
        self.input_terminal = QLineEdit()
        self.input_terminal.setPlaceholderText("Input terminal – type a command and press Enter...")
        self.input_terminal.returnPressed.connect(self.handle_input)

        # === Combine into layout ===
        central_layout.addWidget(splitter)
        central_layout.addWidget(self.input_terminal)

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # === Menu Bar ===
        self._create_menu_bar()

        # === Status Bar ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("Open", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self))

        # Settings menu
        settings_menu = menu_bar.addMenu("Settings")
        settings_menu.addAction(QAction("Preferences", self))

        # Tools menu
        tools_menu = menu_bar.addMenu("Tools")
        tools_menu.addAction(QAction("Tool 1", self))

        # Run menu
        run_menu = menu_bar.addMenu("Run")
        run_menu.addAction(QAction("Start Flow", self))

    def handle_input(self):
        command = self.input_terminal.text().strip()
        if command:
            self.output_terminal.appendPlainText(f"> {command}")
            # You can add more complex logic here
            self.input_terminal.clear()