from typing import Literal

from PySide6.QtWidgets import (
    QGraphicsView, 
    QGraphicsScene,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter
from generate_task import GenerateTask
from chip_widget import Chip, ChipGraphicsItem

ThemeLiteral = Literal["dark"] | Literal["light"]

class GameView(QGraphicsView):

    chip_connected = Signal(ChipGraphicsItem, ChipGraphicsItem)

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.theme: ThemeLiteral = self.main_window.theme


        self.setAcceptDrops(True)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)


        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.sc = QGraphicsScene()
        self.setScene(self.sc)

        self.chips = []

        self.task = GenerateTask()      
        self.task.finished.connect(self.generate_finished)
        self.chip_connected.connect(self.chip_connect)

    def add_chip(self, w: Chip):
        chip = ChipGraphicsItem(w.text(), self.theme)    
        self.sc.addItem(chip)  
        self.chips.append(chip)

    def chip_connect(self, chip1, chip2):
        # if self.task.isRunning():
        #     return
        
        text1 = chip1.toPlainText()
        text2 = chip2.toPlainText()
        chip1.loading = True
        chip2.loading = True
        print("Generting for", text1, text2)        
        self.task.update_text(chip1, chip2)
        self.task.start()

    def generate_finished(self, chip1: ChipGraphicsItem, chip2: ChipGraphicsItem, result: str):
        chip1.loading = False
        chip2.loading = False
        
        scene_pos = chip2.scenePos()

        self.scene().removeItem(chip1)
        self.scene().removeItem(chip2)
        self.chips.remove(chip1)
        self.chips.remove(chip2)

        chip = ChipGraphicsItem(result, self.theme)    
        chip.setPos(scene_pos)
        self.sc.addItem(chip)  
        self.chips.append(chip)

        # check if chip with text already exists or not
        for idx in range(self.main_window.chips_list.count()):
            item = self.main_window.chips_list.item(idx)
            # get the widget from QListWidgetItem
            widget = self.main_window.chips_list.itemWidget(item)
            if widget.text() == result:
                return

        chip = Chip(result, self.add_chip, self.theme)
        self.main_window.chips_list.addChip(chip)  