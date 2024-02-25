from PySide6.QtWidgets import QDialog, QWidget, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QTextEdit, QComboBox
from PySide6.QtCore import Qt 
from configmanager import ConfigManger
from consts import MODELS, DEFAULT_SYSTEM_MSG, DEFAULT_BASE_URL, DEFAULT_MODEL

class Settings(QDialog):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.conf_manager = ConfigManger()
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 500)

        self.heading_layout = QHBoxLayout()
        self.heading_layout.setContentsMargins(0, 0, 0, 0)

        self.heading = QLabel("Settings")
        font = self.heading.font()
        font.setPointSize(24)
        self.heading.setFont(font)
        self.heading_layout.addWidget(self.heading, stretch=2)
        reset_btn = QPushButton("Reset")
        reset_btn.setMinimumHeight(30)
        reset_btn.clicked.connect(self.reset_settings)
        self.heading_layout.addWidget(reset_btn, stretch=1)      


        self.lay = QVBoxLayout()
        self.lay.setSpacing(5)

        self.lay.addLayout(self.heading_layout)  # Add heading_layout to the main layout

        self.models_choice = QComboBox()
        self.models_choice.addItems(MODELS)
        self.models_choice.setCurrentText(self.conf_manager.get_key("model"))
        self.lay.addWidget(QLabel("Model"))
        self.lay.addWidget(self.models_choice)

        self.lay.addWidget(QLabel("Base URL"))
        self.base_url_input = QLineEdit()
        self.base_url_input.setMinimumHeight(30)
        self.base_url_input.setText(self.conf_manager.get_key("base_url"))
        self.base_url_input.setPlaceholderText("Base URL")
        self.lay.addWidget(self.base_url_input)

        self.lay.addWidget(QLabel("System Prompt"))
        self.system_prompt_input = QTextEdit()
        font = self.system_prompt_input.font()
        font.setPointSize(14)
        self.system_prompt_input.setFont(font)
        self.system_prompt_input.setPlaceholderText("System prompt")
        self.system_prompt_input.setText(self.conf_manager.get_key("system_msg"))
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
        self.lay.addLayout(buttons_layout)

        self.setLayout(self.lay)

    def save_settings(self):
        conf = self.conf_manager.get_config()
        conf["model"] = self.models_choice.currentText()
        conf["base_url"] = self.base_url_input.text()
        conf["system_msg"] = self.system_prompt_input.toPlainText()
        self.conf_manager.set_config(conf)
        self.accept()

    def reset_settings(self):
        self.models_choice.setCurrentText(DEFAULT_MODEL)
        self.base_url_input.setText(DEFAULT_BASE_URL)
        self.system_prompt_input.setText(DEFAULT_SYSTEM_MSG)




