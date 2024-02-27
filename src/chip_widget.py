from PySide6.QtWidgets import (
    QGraphicsSceneMouseEvent,
    QGraphicsItem,
    QGraphicsTextItem,
    QLabel
)

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QBrush, QDrag, QLinearGradient
from typing import Literal

ThemeLiteral = Literal["dark"] | Literal["light"]

class Chip(QLabel):

    def __init__(self, text: str, add_chip_func, theme: ThemeLiteral = "light") -> None:
        """        Initialize a custom label with text and theme.

        Args:
            text (str): The text to be displayed on the label.
            add_chip_func: The function to add a chip to the label.
            theme (ThemeLiteral?): The theme of the label. Defaults to "light".


        Note:
            The function sets the text, theme, border radius, alignment, background color, color, style sheet,
            cursor, and fixed height of the label.
        """

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
        """        Handle mouse press event.

        This method handles the mouse press event and adds a chip if the left button is pressed.

        Args:
            ev (QMouseEvent): The mouse event object.
        """

        super().mousePressEvent(ev)

        if ev.button() == Qt.LeftButton:
            self.add_chip_func(self)

    def mouseMoveEvent(self, e):
        """        Handle the mouse move event.

        If the left mouse button is pressed, it initiates a drag action using QDrag and QMimeData.

        Args:
            e (QMouseEvent): The mouse event object.
        """

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)

        super().mouseMoveEvent(e)           

class ChipGraphicsItem(QGraphicsTextItem):

    def __init__(self, text: str, theme: ThemeLiteral = "light") -> None:
        """        Initialize the graphics item with text and theme.

        Args:
            text (str): The text to be displayed.
            theme (ThemeLiteral?): The theme of the graphics item. Defaults to "light".
        """

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
        """        Returns the bounding rectangle of the item, adjusted by -4 on each side.

        This method calculates the bounding rectangle of the item using the super class's boundingRect method,
        and then adjusts the rectangle by -4 on each side.

        Returns:
            QRectF: The adjusted bounding rectangle of the item.
        """

        # calculate
        rect = super().boundingRect()
        return rect.adjusted(-4, -4, 4, 4)
    
    def paint(self, painter, option, widget):
        """        Paint the widget using the specified painter and options.

        This method is responsible for painting the widget using the provided painter and options. It sets the pen and brush colors based on the theme and other attributes of the widget.

        Args:
            painter: QPainter object used for painting.
            option: QStyleOptionGraphicsItem object specifying the style options for the widget.
            widget: QWidget object representing the widget to be painted.
        """

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
        """        Handle the mouse press event in the graphics scene.

        This method is called when a mouse press event occurs in the graphics scene. It sets the holding_down flag to True
        and changes the cursor to a pointing hand cursor. Additionally, it sets the z-value of the object to 1.

        Args:
            event (QGraphicsSceneMouseEvent): The mouse press event object.
        """

        super().mousePressEvent(event)    

        if event.button() == Qt.LeftButton:
            self.holding_down = True
            self.setCursor(Qt.PointingHandCursor)
            self.setZValue(1)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """        Handle the mouse release event for the custom QGraphicsTextItem.

        This method is called when the mouse button is released over the QGraphicsTextItem.
        It checks if the left mouse button was released, sets the cursor to the arrow shape,
        and updates the holding_down flag if it was previously set. Then, it checks for collision
        with other items in the scene and emits a signal if a collision is detected.

        Args:
            event (QGraphicsSceneMouseEvent): The mouse release event object.

            chip_connected: If a collision is detected, this signal is emitted with the current
            QGraphicsTextItem and the collided item as arguments.
        """

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
        """        Handle the mouse move event for the QGraphicsTextItem.

        This method is responsible for handling the mouse move event for the QGraphicsTextItem. It checks for collision
        with other items in the scene and sets the merge_clr attribute accordingly.

        Args:
            event (QGraphicsSceneMouseEvent): The mouse move event.
        """

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