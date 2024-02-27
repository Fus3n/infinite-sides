from typing import Literal
import sys, os, json

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow, 
    QHBoxLayout,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QLineEdit,
    QPushButton,
    QDialog,
    QMessageBox,
    QLabel
)

from PySide6.QtCore import Qt
import qdarkstyle

from chip_widget import Chip
from game_view import GameView
from settings import Settings

from configmanager import ConfigManger

class ChipList(QListWidget):

    def add_chip(self, chip: Chip):
        """        Add a chip to the list.

        This method adds a chip to the list by creating a QListWidgetItem with the size hint of the chip and setting it as the item widget.

        Args:
            chip (Chip): The chip to be added to the list.
        """

        item = QListWidgetItem()
        item.setSizeHint(chip.sizeHint())  
        item.setFlags(Qt.NoItemFlags)
        self.addItem(item)
        self.setItemWidget(item, chip)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        """        Initialize the InfiniteSides application.

        This method sets up the InfiniteSides application by initializing various components such as the game view, sidebar, buttons, chip list, search bar, and menu.
        """

        super().__init__()

        self.setMouseTracking(True)
        self.conf = ConfigManger()
        self.setWindowTitle("InfiniteSides")
        self.setMinimumSize(1000, 700)
        # set theme here
        self.theme: Literal["dark"] | Literal["light"] = "dark"

        # Game
        self.game_file = "./game-data.json"     

        self.frame = QFrame()
        
        self.lay = QHBoxLayout()
        self.frame.setLayout(self.lay)

        self.game_view = GameView(self)
        self.lay.addWidget(self.game_view)
        

        self.sidebar = QVBoxLayout()
        
        clear_btn = QPushButton("Clear")
        clear_btn.setMinimumHeight(30)
        clear_btn.clicked.connect(self.game_view.sc.clear)
        reset_btn = QPushButton("Reset")
        reset_btn.setMinimumHeight(30)
        reset_btn.clicked.connect(self.reset_list)

        btn_group = QHBoxLayout()
        btn_group.addWidget(clear_btn)
        btn_group.addWidget(reset_btn)


        self.chips_list = ChipList()
        self.chips_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.chips_list.setFlow(QListWidget.Flow.LeftToRight)
        self.chips_list.setWrapping(True)
        self.chips_list.setMaximumWidth(250)
        self.chips_list.setSpacing(5)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setMaximumWidth(250)
        self.search_bar.setMinimumHeight(40)
        self.search_bar.textChanged.connect(self.filterItems)

        self.sidebar.addLayout(btn_group)
        self.sidebar.addWidget(self.chips_list)
        self.sidebar.addWidget(self.search_bar)

        self.load_game_data()

        self.lay.addLayout(self.sidebar)
        self.setCentralWidget(self.frame)

        self.init_menu()

    def load_game_data(self):
        """        Load game data from the specified file.

        If the game file exists, it loads the chips and returns.
        If the game file does not exist, it populates default chips and saves them.

        Raises:
            FileNotFoundError: If the game file does not exist.
        """

        if os.path.exists(self.game_file):
            self.load_chips()
            return

        self.populate_default_chips()      
        self.save_chips()

    def load_chips(self):
        """        Load chips from a JSON file and populate the chips list.

        If the JSON file is empty, it populates the chips list with default chips.

        Args:
            self (object): The current instance of the class.


        Raises:
            FileNotFoundError: If the specified game file does not exist.
            json.JSONDecodeError: If the JSON file is not valid.
        """

        with open(self.game_file, "r") as f:
            data = json.load(f)
            if not data:
                self.populate_default_chips()
                return
            
            for chip in data:
                chip = Chip(chip, self.game_view.add_chip, self.theme)
                self.chips_list.add_chip(chip)

    def save_chips(self):
        """        Save the chips list to a file.

        This function retrieves the chips from the chips list, and then saves them to a file in JSON format.

        Args:
            self: The instance of the class.
        """

        chips = []
        for idx in range(self.chips_list.count()):
            item = self.chips_list.item(idx)
            widget = self.chips_list.itemWidget(item)
            chips.append(widget.text())
            
        with open(self.game_file, "w") as f:
            json.dump(chips, f)

    def populate_default_chips(self):
        """        Populate the default chips for the game.

        This function creates default chips for Earth, Water, Fire, and Air and adds them to the chips list.

        Args:
            self (object): The current instance of the class.
        """

        earth_chip = Chip("🌍 Earth", self.game_view.add_chip, self.theme)
        water_chip = Chip("💧 Water",self.game_view.add_chip, self.theme)
        fire_chip = Chip("🔥 Fire", self.game_view.add_chip, self.theme)
        air_chip = Chip("💨 Air", self.game_view.add_chip, self.theme)

        self.chips_list.add_chip(earth_chip)
        self.chips_list.add_chip(water_chip)
        self.chips_list.add_chip(fire_chip)
        self.chips_list.add_chip(air_chip)

    def reset_list(self):
        """        Display a confirmation dialog and reset the list if user confirms.

        This function displays a confirmation dialog to the user asking if they want to reset the list. If the user confirms
        the reset, the function clears the chips list, populates it with default chips, and clears the game view.
        """

        dialog = QMessageBox()
        dialog.setWindowTitle('Reset Confirmation')
        dialog.setText('Are you sure you want to reset?')
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)

        # Executing the dialog and getting the result
        result = dialog.exec()
        if result == QMessageBox.Yes:
            self.chips_list.clear()
            self.populate_default_chips()
            self.game_view.sc.clear()

    def filterItems(self):
        """        Filter the items in the chips list based on the search text.

        This function filters the items in the chips list based on the search text entered in the search bar. It iterates through each item in the list, retrieves the text from the associated widget, and compares it with the search text. If the search text is found in the item's text, the item is displayed; otherwise, it is hidden.

        Args:
            self: The object instance.
        """

        search_text = self.search_bar.text()
        for idx in range(self.chips_list.count()):
            item = self.chips_list.item(idx)
            widget = self.chips_list.itemWidget(item)
            if search_text.lower() in widget.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
        
        self.game_view.update()

    def init_menu(self):
        """        Initialize the application menu and theme menu.

        This method sets up the application menu and theme menu in the main window. It adds actions for 'Settings' and 'Reset All' in the app menu, and 'Dark' and 'Light' themes in the theme menu.

        Args:
            self: The instance of the main window.
        """

        menu = self.menuBar()
        app_menu = menu.addMenu("App")
        theme_menu = menu.addMenu("Theme")

        # App menu
        settings_window_action = app_menu.addAction("Settings")
        settings_window_action.triggered.connect(self.open_settings)

        reset_all_action = app_menu.addAction("Reset All")
        reset_all_action.triggered.connect(self.reset_chips)

        # Theme menu
        dark_action = theme_menu.addAction("Dark")
        dark_action.triggered.connect(self.set_theme_dark)

        light_action = theme_menu.addAction("Light")
        light_action.triggered.connect(self.set_theme_light)

    def set_theme_dark(self):
        """        Set the theme to dark and apply the corresponding style sheet to the QApplication instance.

        This method sets the theme attribute to "dark" and applies the dark theme style sheet to the QApplication instance.

        Args:
            self: The instance of the class.
        """

        self.theme = "dark"
        QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet())

    def set_theme_light(self):
        """        Set the theme to light.

        This method sets the theme attribute to "light" and resets the style sheet of the QApplication instance.

        Args:
            self: The instance of the class.
        """

        self.theme = "light"
        QApplication.instance().setStyleSheet("")
    
    def set_base_url(self):
        """        Set the base URL for the application.

        This method creates a dialog window to allow the user to set the base URL for the application.
        It prompts the user to input the base URL and saves the input in the application configuration.

        Args:
            self: The instance of the class.
        """

        dialog = QDialog()
        dialog.setWindowTitle("Set Base URL")
        dialog.setFixedWidth(300)
        #disabel resize

        layout = QVBoxLayout()

        base_url_label = QLabel("Base URL:")
        base_url_label.setMaximumHeight(20)
        base_url_input = QLineEdit()
        current_base_url = self.conf.get_key("base_url")
        base_url_input.setPlaceholderText(current_base_url)

        layout.addWidget(base_url_label)
        layout.addWidget(base_url_input)

        dialog.setLayout(layout)

        # Add buttons to the dialog
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)

        dialog.setMaximumHeight(dialog.minimumHeight())


        # Show the dialog and wait for the user to click one of the buttons
        if dialog.exec() == QDialog.Accepted:
            base_url = base_url_input.text()
            if base_url == "":
                return

            self.conf.set_base_url(base_url.strip())            

    def show_error(self, msg):
        """        Display an error message using a QMessageBox.

        Args:
            self: The instance of the class.
            msg (str): The error message to be displayed.
        """

        QMessageBox.critical(self, "Error", msg)

    def open_settings(self):
        """        Open the settings dialog.

        This function creates an instance of the Settings class and executes the settings dialog.

        Args:
            self: The instance of the current class.
        """

        settings = Settings(self)
        settings.exec()

    def reset_chips(self):
        """        Reset all the chips and the game view.

        This method displays a confirmation message to the user and if the user confirms, it clears the chips list,
        populates default chips, clears the game view, saves the chips, and updates the game view.
        """

        msg = QMessageBox()
        msg.setWindowTitle("Reset Confirmation")
        msg.setText("Are you sure you want to reset everything? This will remove all the cips you created.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = msg.exec()
        if result == QMessageBox.Yes:
            self.chips_list.clear()
            self.populate_default_chips()
            self.game_view.sc.clear()
            self.save_chips()
            self.game_view.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    if window.theme == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

    window.show()
    app.exec()
