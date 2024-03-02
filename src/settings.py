from PySide6.QtWidgets import (
    QDialog,
    QWidget, 
    QPushButton, 
    QHBoxLayout, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QTextEdit, 
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt 
from configmanager import ConfigManger
from consts import MODELS, DEFAULT_SYSTEM_MSG, DEFAULT_BASE_URL, DEFAULT_MODEL, DEFAULT_EXAMPLES, DEFAULT_CHIPS
from example_entry_widget import ExampleEntry, ChipEntry

class Settings(QDialog):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.conf_manager = ConfigManger()
        self.setWindowTitle("Settings")
        self.setMinimumSize(980, 650)

        self.heading_layout = QHBoxLayout()
        self.heading_layout.setContentsMargins(0, 0, 0, 0)

        self.heading = QLabel("Settings")
        font = self.heading.font()
        font.setPointSize(24)
        self.heading.setFont(font)
        self.heading_layout.addWidget(self.heading, stretch=2)
        reset_btn = QPushButton("Reset")
        reset_btn.setToolTip("Restore all the fields with default values\nbut won't be saved unless save button is pressed.")
        reset_btn.setMinimumHeight(30)
        reset_btn.clicked.connect(self.reset_settings)
        self.heading_layout.addWidget(reset_btn, stretch=1)      

        self.section_layout = QHBoxLayout()

        self.examples_lay = QVBoxLayout()
        self.examples_list = QListWidget()
        self.examples_list.setFixedWidth(280)

        add_example_btn = QPushButton("Add Example")
        add_example_btn.setToolTip("Add an example with the given format\nto make it easier for AI to understand the game.")
        add_example_btn.setMinimumHeight(30)
        add_example_btn.clicked.connect(self.add_example)

        self.examples_lay.addWidget(add_example_btn)
        self.examples_lay.addWidget(self.examples_list)

        self.chips_lay = QVBoxLayout()
        self.chips_list = QListWidget()
        self.chips_list.setFixedWidth(180)

        add_chip_btn = QPushButton("Add Default Chip")
        add_chip_btn.setToolTip("Add a chip with default text and emoji\nthese will only show up after you reset the game.")
        add_chip_btn.setMinimumHeight(30)
        add_chip_btn.clicked.connect(self.add_chip)

        self.chips_lay.addWidget(add_chip_btn)
        self.chips_lay.addWidget(self.chips_list)

        conf = self.conf_manager.get_config()

        # populate list
        for example in conf["examples"]:
            self.add_example_entry(example["from_str"], example["result_str"])

        for chip in conf["default_chips"]:
            self.add_chip_text(chip)

        self.lay = QVBoxLayout()
        self.lay.setSpacing(5)

        self.lay.addLayout(self.heading_layout)  # Add heading_layout to the main layout

        self.models_choice = QComboBox()
        self.models_choice.addItems(MODELS)
        self.models_choice.setCurrentText(conf["model"])
        self.lay.addWidget(QLabel("Model"))
        self.lay.addWidget(self.models_choice)

        self.lay.addWidget(QLabel("Base URL"))
        self.base_url_input = QLineEdit()
        self.base_url_input.setMinimumHeight(30)
        self.base_url_input.setText(conf["base_url"])
        self.base_url_input.setPlaceholderText("Base URL")
        self.lay.addWidget(self.base_url_input)

        self.lay.addWidget(QLabel("System Prompt"))
        self.system_prompt_input = QTextEdit()
        font = self.system_prompt_input.font()
        font.setPointSize(14)
        self.system_prompt_input.setFont(font)
        self.system_prompt_input.setPlaceholderText("System prompt")
        self.system_prompt_input.setText(conf["system_msg"])
        self.lay.addWidget(self.system_prompt_input)


        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ok_button = QPushButton("Save")
        ok_button.setMinimumHeight(30)
        ok_button.clicked.connect(self.save_settings)

        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(30)

        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        self.section_layout.addLayout(self.lay)
        self.section_layout.addLayout(self.examples_lay)
        self.section_layout.addLayout(self.chips_lay)

        self.dialog_lay = QVBoxLayout()

        self.dialog_lay.addLayout(self.section_layout)
        self.dialog_lay.addLayout(buttons_layout)

        self.setLayout(self.dialog_lay)

    def save_settings(self):
        conf = self.conf_manager.get_config()
        conf["model"] = self.models_choice.currentText()
        conf["base_url"] = self.base_url_input.text()
        conf["system_msg"] = self.system_prompt_input.toPlainText()

        conf["examples"] = []   
        for i in range(self.examples_list.count()):
            item = self.examples_list.item(i)
            example_entry: ExampleEntry = self.examples_list.itemWidget(item)
            conf["examples"].append(
                {
                    "from_str": example_entry.from_input.text(),
                    "result_str": example_entry.result_input.text()
                }
            )
        
        conf["default_chips"] = []
        for i in range(self.chips_list.count()):
            item = self.chips_list.item(i)
            widget = self.chips_list.itemWidget(item)
            conf["default_chips"].append(widget.text())

        self.conf_manager.set_config(conf)
        self.accept()

    def reset_settings(self):
        self.models_choice.setCurrentText(DEFAULT_MODEL)
        self.base_url_input.setText(DEFAULT_BASE_URL)
        self.system_prompt_input.setText(DEFAULT_SYSTEM_MSG)
        self.reset_examples()
        self.reset_chips()

    def reset_examples(self):
        self.examples_list.clear()
        for example in DEFAULT_EXAMPLES:
            self.add_example_entry(example["from_str"], example["result_str"])

    def reset_chips(self):
        self.chips_list.clear()
        for chip in DEFAULT_CHIPS:
            self.add_chip_text(chip)

    def add_example_entry(self, from_txt: str, result_txt: str):
        item = QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)
        item_edit = ExampleEntry(from_txt, result_txt, item)
        item.setSizeHint(item_edit.sizeHint())  
        self.examples_list.addItem(item)
        self.examples_list.setItemWidget(item, item_edit)

    def remove_item(self, item: QListWidgetItem):
        self.examples_list.takeItem(self.examples_list.row(item))
        self.conf_manager.remove_example(item.text())
        item.setHidden(True)
        self.examples_list.update()

    def add_example(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Example")
        dialog.setFixedWidth(400)

        dialog_lay = QVBoxLayout()
        dialog_lay.setSpacing(5)
        dialog.setLayout(dialog_lay)

        from_label = QLabel("From")
        from_input = QLineEdit()
        from_input.setMinimumHeight(30)
        from_input.setPlaceholderText("\ud83c\udf0d Earth + \ud83d\udca7 Water")
        from_lay = QHBoxLayout()
        from_lay.addWidget(from_label)
        from_lay.addWidget(from_input)

        result_label = QLabel("Result:")
        result_input = QLineEdit()
        result_input.setMinimumHeight(30)
        result_input.setPlaceholderText("\ud83c\udf31 Plant")
        result_lay = QHBoxLayout()
        result_lay.addWidget(result_label)
        result_lay.addWidget(result_input)

        dialog_lay.addLayout(from_lay)
        dialog_lay.addLayout(result_lay)


        buttons_lay = QHBoxLayout()
        buttons_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        ok_button = QPushButton("Save")
        ok_button.setMinimumHeight(30)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(30)
        cancel_button.clicked.connect(dialog.reject)
        buttons_lay.addWidget(ok_button)
        buttons_lay.addWidget(cancel_button)

        dialog_lay.addLayout(buttons_lay)
        dialog.setFixedHeight(dialog.sizeHint().height())

        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            from_txt = from_input.text()
            result_txt = result_input.text()
            self.add_example_entry(from_txt, result_txt)

    def add_chip_text(self, txt: str):
        item = QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)
        item_edit = ChipEntry(txt, item)
        item.setSizeHint(item_edit.sizeHint())  
        self.chips_list.addItem(item)
        self.chips_list.setItemWidget(item, item_edit)

    def add_chip(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Chip")
        dialog.setFixedWidth(400)

        dialog_lay = QVBoxLayout()
        dialog_lay.setSpacing(5)
        dialog.setLayout(dialog_lay)

        lbl = QLabel("Chip Text And Emoji")
        chip_inp = QLineEdit()
        chip_inp.setMinimumHeight(30)
        chip_inp.setPlaceholderText("🌳 Tree")
        
        dialog_lay.addWidget(lbl)
        dialog_lay.addWidget(chip_inp)

        buttons_lay = QHBoxLayout()
        buttons_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        ok_button = QPushButton("Save")
        ok_button.setMinimumHeight(30)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(30)
        cancel_button.clicked.connect(dialog.reject)
        buttons_lay.addWidget(ok_button)
        buttons_lay.addWidget(cancel_button)

        dialog_lay.addLayout(buttons_lay)
        dialog.setFixedHeight(dialog.sizeHint().height())

        if dialog.exec() == QDialog.DialogCode.Accepted:
            chip_txt = chip_inp.text()
            self.add_chip_text(chip_txt)