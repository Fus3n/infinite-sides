from typing import Literal
import sys

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

from configmanager import ConfigManger

class ChipList(QListWidget):

    def addChip(self, chip: Chip):
        item = QListWidgetItem()
        item.setSizeHint(chip.sizeHint())  
        item.setFlags(Qt.NoItemFlags)
        self.addItem(item)
        self.setItemWidget(item, chip)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.conf = ConfigManger()

        self.setWindowTitle("InfCraft")
        self.setMinimumSize(1000, 700)
        # set theme here
        self.theme: Literal["dark"] | Literal["light"] = "dark"

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

        self.populate_default_chips()

        self.lay.addLayout(self.sidebar)
        self.setCentralWidget(self.frame)

        self.init_menu()

    def populate_default_chips(self):
        earth_chip = Chip("🌍 Earth", self.game_view.add_chip, self.theme)
        water_chip = Chip("💧 Water",self.game_view.add_chip, self.theme)
        fire_chip = Chip("🔥 Fire", self.game_view.add_chip, self.theme)
        air_chip = Chip("💨 Air", self.game_view.add_chip, self.theme)

        self.chips_list.addChip(earth_chip)
        self.chips_list.addChip(water_chip)
        self.chips_list.addChip(fire_chip)
        self.chips_list.addChip(air_chip)

    def reset_list(self):
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
        file_menu = menu.addMenu("Settings")
        theme_menu = menu.addMenu("Theme")

        # File menu
        system_prmpt_action = file_menu.addAction("System Prompt")
        system_prmpt_action.triggered.connect(lambda: print("sys"))

        select_model_action = file_menu.addAction("Select Model")
        select_model_action.triggered.connect(lambda: print("sys"))

        set_base_url_action = file_menu.addAction("Set Base URL")
        set_base_url_action.triggered.connect(self.set_base_url)


        # Theme menu
        dark_action = theme_menu.addAction("Dark")
        dark_action.triggered.connect(self.set_theme_dark)

        light_action = theme_menu.addAction("Light")
        light_action.triggered.connect(self.set_theme_light)

    def set_theme_dark(self):
        self.theme = "dark"
        QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet())

    def set_theme_light(self):
        self.theme = "light"
        QApplication.instance().setStyleSheet("")
        print('w')
    
    def set_base_url(self):
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

            self.conf.set_base_url(base_url)            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    if window.theme == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    app.exec()
