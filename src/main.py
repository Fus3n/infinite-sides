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

from consts import DEFAULT_CHIPS

class ChipList(QListWidget):

    def add_chip(self, chip: Chip):
        item = QListWidgetItem()
        item.setSizeHint(chip.sizeHint())  
        item.setFlags(Qt.NoItemFlags)
        self.addItem(item)
        self.setItemWidget(item, chip)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setMouseTracking(True)
        self.conf_manager = ConfigManger()
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
        reset_btn.clicked.connect(self.reset_chip_list)

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
        if os.path.exists(self.game_file):
            self.load_chips()
            return

        self.populate_default_chips()      
        self.save_chips()

    def load_chips(self):
        with open(self.game_file, "r") as f:
            data = json.load(f)
            if not data:
                self.populate_default_chips()
                return
            
            for chip in data:
                chip = Chip(chip, self.game_view.add_chip, self.theme)
                self.chips_list.add_chip(chip)

    def save_chips(self):
        chips = []
        for idx in range(self.chips_list.count()):
            item = self.chips_list.item(idx)
            widget = self.chips_list.itemWidget(item)
            chips.append(widget.text())

        with open(self.game_file, "w") as f:
            json.dump(chips, f)

    def populate_default_chips(self):
        chips = self.conf_manager.get_value("default_chips")
        for chip in chips:
            c = Chip(chip, self.game_view.add_chip, self.theme)
            self.chips_list.add_chip(c)

    def filterItems(self):
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
        menu = self.menuBar()
        app_menu = menu.addMenu("App")
        theme_menu = menu.addMenu("Theme")

        # App menu
        settings_window_action = app_menu.addAction("Settings")
        settings_window_action.triggered.connect(self.open_settings)

        reset_all_action = app_menu.addAction("Reset All")
        reset_all_action.triggered.connect(self.reset_chip_list)

        # Theme menu
        dark_action = theme_menu.addAction("Dark")
        dark_action.triggered.connect(self.set_theme_dark)

        light_action = theme_menu.addAction("Light")
        light_action.triggered.connect(self.set_theme_light)

    def set_theme_dark(self):
        self.theme = "dark"
        QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

    def set_theme_light(self):
        self.theme = "light"
        QApplication.instance().setStyleSheet("")
    
    def set_base_url(self):
        dialog = QDialog()
        dialog.setWindowTitle("Set Base URL")
        dialog.setFixedWidth(300)
        #disabel resize

        layout = QVBoxLayout()

        base_url_label = QLabel("Base URL:")
        base_url_label.setMaximumHeight(20)
        base_url_input = QLineEdit()
        current_base_url = self.conf_manager.get_value("base_url")
        base_url_input.setPlaceholderText(current_base_url)

        layout.addWidget(base_url_label)
        layout.addWidget(base_url_input)

        dialog.setLayout(layout)

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

        if dialog.exec() == QDialog.Accepted:
            base_url = base_url_input.text()
            if base_url == "":
                return

            self.conf_manager.set_base_url(base_url.strip())            

    def show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

    def open_settings(self):
        settings = Settings(self)
        settings.exec()

    def reset_chip_list(self):
        dialog = QMessageBox()
        dialog.setWindowTitle('Reset Confirmation')
        dialog.setText("Are you sure you want to reset everything? This will also remove all the chips you created.")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)

        result = dialog.exec()
        if result == QMessageBox.Yes:
            self.chips_list.clear()
            self.populate_default_chips()
            self.game_view.sc.clear()
            self.save_chips()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    if window.theme == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

    window.show()
    app.exec()
