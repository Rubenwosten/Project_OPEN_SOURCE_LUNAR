# Import necessary PyQt5 widgets and classes
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLineEdit, QFileSystemModel, QTreeView,
    QSplitter, QMenuBar, QAction, QStatusBar
)
from PyQt5.QtCore import Qt, QDir
from block_diagram_view import BlockDiagramView  # Custom canvas widget for drawing blocks

# Main application window that opens a project view
class MainProjectWindow(QMainWindow):
    def __init__(self, project_path):
        super().__init__()
        self.setWindowTitle("Analog IC Toolchain - Project View")  # Set title
        self.setGeometry(200, 100, 1200, 800)  # Define window size and position

        self.project_path = project_path  # Save project path for internal reference

        # === Central layout for the whole window ===
        central_widget = QWidget()
        central_layout = QVBoxLayout()

        # === Splitter separates folder view and the diagram/terminal area ===
        splitter = QSplitter(Qt.Horizontal)  # Horizontal splitter

        # === Folder view using QFileSystemModel ===
        self.tree_view = QTreeView()
        self.model = QFileSystemModel()                   # File system model for the tree
        self.model.setRootPath(project_path)              # Set root directory
        self.tree_view.setModel(self.model)               # Attach model to view
        self.tree_view.setRootIndex(self.model.index(project_path))  # Focus on project directory
        self.tree_view.setColumnWidth(0, 250)             # Widen the name column

        splitter.addWidget(self.tree_view)  # Add folder view to the splitter

        # === Block diagram view (replaces the output terminal) ===
        self.diagram_view = BlockDiagramView()            # Custom block diagram widget
        splitter.addWidget(self.diagram_view)             # Add to splitter
        splitter.setStretchFactor(1, 3)                   # Give more space to diagram view

        # === Input terminal to type commands ===
        self.input_terminal = QLineEdit()
        self.input_terminal.setPlaceholderText("Input terminal – type a command and press Enter...")
        self.input_terminal.returnPressed.connect(self.handle_input)  # Trigger on Enter

        # === Assemble layout ===
        central_layout.addWidget(splitter)
        central_layout.addWidget(self.input_terminal)     # Input field at the bottom

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)             # Set central widget of the window

        # === Create menu bar ===
        self._create_menu_bar()

        # === Create status bar ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    # Menu bar with common menu items
    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("Open", self))        # Placeholder: no slot connected yet
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self))

        # Settings menu
        settings_menu = menu_bar.addMenu("Settings")
        settings_menu.addAction(QAction("Preferences", self))

        # Tools menu
        tools_menu = menu_bar.addMenu("Tools")
        tools_menu.addAction(QAction("Tool 1", self))     # Placeholder for tool feature

        # Run menu
        run_menu = menu_bar.addMenu("Run")
        run_menu.addAction(QAction("Start Flow", self))   # Placeholder for starting a design flow

    # Handle commands typed into the input terminal
    def handle_input(self):
        command = self.input_terminal.text().strip()
        if command:
            self.output_terminal.appendPlainText(f"> {command}")  # Display in output (commented out above)
            self.input_terminal.clear()  # Clear after executing