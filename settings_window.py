from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent #reference to the window where settings is called
        self.setWindowTitle("Settings") #title of settings window
        self.setGeometry(400, 250, 300, 150) #x , y coordinates and size of the window
        self.init_ui() #go to ui generation

    def init_ui(self):
        layout = QVBoxLayout() #create layout

        self.combo = QComboBox() # first settings dropdown menu
        self.combo.addItems(["-----", "Mixed Signal", "Analog Signal", "Digital Signal"]) #items of dropdown menu
        self.combo.setCurrentText(self.parent.design_type) #set current setting
        self.combo.currentIndexChanged.connect(self.update_setting) #update the setting in main file

        self.automation_combo = QComboBox() # second settings dropdown menu
        self.automation_combo.addItems(["-----", "Fully", "Semi", "Complete user controll"]) # items 
        self.automation_combo.setCurrentText(self.parent.automation_level)# set current setting
        self.automation_combo.currentIndexChanged.connect(self.update_setting) # update current setting


        #add the layout components in order from top to bottom
        layout.addWidget(QLabel("Select design type:")) 
        layout.addWidget(self.combo)
        layout.addWidget(QLabel("Select automation level:"))
        layout.addWidget(self.automation_combo)

        self.setLayout(layout)

    def update_setting(self): #update the settings
        selected = self.combo.currentText() #retrieves setting
        selected_auto = self.automation_combo.currentText() #retrieves setting
        self.parent.design_type = selected #updates settings in the main file
        self.parent.automation_level = selected_auto #updates settings in the main file
        self.parent.save_config()