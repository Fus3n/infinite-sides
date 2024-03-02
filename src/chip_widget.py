from PySide6.QtWidgets import (
    QGraphicsSceneMouseEvent,
    QGraphicsItem,
    QGraphicsTextItem,
    QLabel,
    QGraphicsDropShadowEffect
)

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QBrush, QDrag, QLinearGradient
from typing import Literal

ThemeLiteral = Literal["dark"] | Literal["light"]

class Chip(QLabel):

    def __init__(self, text: str, add_chip_func, theme: ThemeLiteral = "light") -> None:
        super().__init__(text)
        self.add_chip_func = add_chip_func
        self.theme = theme
        self.border_radius = 10
        self.setAlignment(Qt.AlignCenter)
        

        backgroundClr = QColor(255, 255, 255) if self.theme == "light" else QColor(0, 0, 0)
        color = QColor(0, 0, 0) if self.theme == "light" else QColor(255, 255, 255)

        self.setStyleSheet(f"""
            background-color: {backgroundClr.name()};
            padding: 5px;
            padding-left: 10px;
            padding-right: 10px;
            border-radius: 10px;       
            color: {color.name()};
            border: 1px solid gray;
        """)
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)   

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super().mousePressEvent(ev)

        if ev.button() == Qt.LeftButton:
            self.add_chip_func(self)
          

class ChipGraphicsItem(QGraphicsTextItem):

    def __init__(self, text: str, theme: ThemeLiteral = "light") -> None:
        super().__init__(text)
        self.theme = theme
        self.loading = False
        self.setFlag(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable) 

        self.holding_down = False
        self.base_theme_clr = QColor(255, 255, 255) if self.theme == "light" else QColor(0, 0, 0)

        self.selected_gradient = QLinearGradient(self.boundingRect().topLeft(), self.boundingRect().bottomRight())
        self.selected_gradient.setColorAt(0, self.base_theme_clr)
        # inverted with 50 percent
        self.selected_gradient.setColorAt(1, QColor(0, 0, 255, 50))

        self.merge_gradient = QLinearGradient(self.boundingRect().topLeft(), self.boundingRect().bottomRight())
        self.merge_gradient.setColorAt(0, self.base_theme_clr)
        self.merge_gradient.setColorAt(1, QColor(0, 255, 0, 50))

        self.merge_clr = False


    def boundingRect(self):
        # calculate
        rect = super().boundingRect()
        return rect.adjusted(-4, -4, 4, 4)
    
    def paint(self, painter, option, widget):
        r = self.boundingRect()

        themed_bg_color = None
        if self.theme == "light":
            painter.setPen(QPen(QColor(0, 0, 0)))
            themed_bg_color = QBrush(QColor(255, 255, 255))
        elif self.theme == "dark":
            painter.setPen(QPen(QColor(255, 255, 255)))
            themed_bg_color = QBrush(QColor(0, 0, 0))


        if self.loading:
            painter.setBrush(QColor("#828282"))
        elif self.holding_down:
            painter.setBrush(self.selected_gradient)
        elif self.merge_clr:
            painter.setBrush(self.merge_gradient)
        else:
            painter.setBrush(themed_bg_color)
        

        painter.drawRoundedRect(r, 8, 8)
        painter.drawText(r, Qt.AlignCenter, self.toPlainText())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)    

        if event.button() == Qt.LeftButton:
            self.holding_down = True
            self.setCursor(Qt.PointingHandCursor)
            self.setZValue(1)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)

        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)

            if self.holding_down:
                self.holding_down = False

        for item in self.scene().items():
            # check if item bounding touching current
            if item == self:
                continue

            if self.collidesWithItem(item):
                # print(f"{self.toPlainText()} is touching {item.toPlainText()}")
                for view in self.scene().views():
                    view.chip_connected.emit(self, item)
                return

        self.setZValue(0)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        for item in self.scene().items():
            # check if item bounding touching current
            if item == self:
                continue

            if self.collidesWithItem(item):
                # print(f"{self.toPlainText()} is touching {item.toPlainText()}")
                item.merge_clr = True
                return
            else:
                item.merge_clr = False