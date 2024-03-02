from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout, 
    QLineEdit, 
    QPushButton
)

class ExampleEntry(QFrame):

    def __init__(self, from_text: str, result_text: str, item) -> None:
        super().__init__()
        self.item = item
        self.from_text = from_text
        self.result_text = result_text

        lay = QHBoxLayout()

        self.from_input = QLineEdit(self.from_text)
        self.result_input = QLineEdit(self.result_text)
        self.result_input.setMaximumWidth(100)
        dlt_btn = QPushButton("X")
        dlt_btn.setMinimumWidth(20)
        dlt_btn.clicked.connect(self.remove_item)

        lay.addWidget(self.from_input, stretch=2)
        lay.addWidget(self.result_input, stretch=1)
        lay.addWidget(dlt_btn)

        self.setLayout(lay)

    def remove_item(self):
        l = self.item.listWidget()
        it = l.row(self.item)
        l.takeItem(it)

class ChipEntry(QFrame):

    def __init__(self, text: str, item) -> None:
        super().__init__()
        self.item = item

        lay = QHBoxLayout()

        self.text_input = QLineEdit(text)
        dlt_btn = QPushButton("X")
        dlt_btn.setMinimumWidth(20)
        dlt_btn.clicked.connect(self.remove_item)

        lay.addWidget(self.text_input)
        lay.addWidget(dlt_btn)

        self.setLayout(lay)

    def remove_item(self):
        l = self.item.listWidget()
        it = l.row(self.item)
        l.takeItem(it)

    def text(self):
        return self.text_input.text()