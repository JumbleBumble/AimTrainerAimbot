import sys
import pyautogui
import threading
from library.AutoAimTrainer import AimTrainer as AutoAimTrainer
from library.region import PositionDialog
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
    QColorDialog,
    QSpinBox,
    QHBoxLayout 
)
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.open,self.aimbot_active = False, False
        self.thread,self.color = None, None
        self.pos_dialog = PositionDialog()
        self.top_left, self.bottom_right = [0, 0], [0, 0]
        self.x_offset, self.y_offset = 0, 0
        self.initUI()

    #Opens color prompt and collects the values
    def get_color(self):
        color = QColorDialog.getColor()
        red_value = color.red()
        green_value = color.green()
        blue_value = color.blue()
        self.color = (red_value, green_value, blue_value)

        self.color_label.setText(f"RGB: ({red_value}, {green_value}, {blue_value})")

    # Used to retrieve the region positions
    def collect_region(self):
        if not self.open:
            self.pos_dialog.show()
            self.region_button.setText("Get Region Positions")

        if self.open:
            self.top_left, self.bottom_right = self.pos_dialog.get_region()
            self.pos_dialog.hide()
            self.region_label.setText(
                f"Region: ({self.top_left[0]}, {self.top_left[1]}) to ({self.bottom_right[0]}, {self.bottom_right[1]})"
            )
        self.open = not self.open

    # Loops find_color from AutoAimTrainer
    def aimbot(self):
        try:
            while self.aimbot_active:
                AutoAimTrainer.find_color(
                    self.color,
                    x_offset = self.x_offset,
                    y_offset = self.y_offset,
                    x_min=self.top_left[0],
                    y_min=self.top_left[1],
                    x_max=self.bottom_right[0],
                    y_max=self.bottom_right[1],
                )
        except (KeyboardInterrupt, pyautogui.FailSafeException): 
            self.aimbot_active = False
            self.aimbot_button.setText("Start Aimbot")
            return

    #Handles starting the aimbot and ending it
    def start_aimbot(self):
        self.aimbot_active = not self.aimbot_active
        if not self.color:
            return self.aimbot_button.setText("Missing Color")
        
        if self.aimbot_active:
            self.thread = threading.Thread(target=self.aimbot)

            if self.thread:
                if self.thread.is_alive(): self.thread.join()
                self.aimbot_button.setText("Stop Aimbot")
                self.thread.start()
        else:
            self.aimbot_button.setText("Start Aimbot")
            if self.thread:
                if self.thread.is_alive(): self.thread.join()

    def initUI(self):
        self.setWindowTitle("Aim Trainer Aimbot")
        self.setFixedSize(350, 150)
        self.setStyleSheet(
            """
        QMainWindow {
            background-image: url(images/main-background.png);
        }

        QLabel {
            border-radius: 2px;
            background-color: #343a40; 
            color: #ffffff; 
            max-height: 20px;
        }

        QPushButton {
            border-radius: 2px;
            border: 1px solid #000000;
            background-color: #007bff; 
            color: #ffffff;
            padding: 4px;
        }

        QPushButton:hover {
            background-color: #0056aa; 
        }

        QSpinBox {
            border: 1px solid #000000; 
            background-color: #ffffff; 
            color: #000000; 
        }

        QSpinBox::up-button {
            background-image: url(images/ArrowUp.png);
         
      
        }

        QSpinBox::down-button {
            background-image: url(images/ArrowDown.png);
            background-repeat: none;
            margin-left: 1px;
            margin-bottom: 1px;

        }
        """
        )
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        (
            self.region_label,
            self.color_label,
            self.color_button,
            self.region_button,
            self.aimbot_button,
        ) = (
            QLabel("Region: (0, 0) to (0, 0)"),
            QLabel("RGB: (0,0,0)"),
            QPushButton("Pick Color"),
            QPushButton("Open Region Window"),
            QPushButton("Start Aimbot"),
        )
        self.region_label.setAlignment(Qt.AlignCenter)
        self.color_label.setAlignment(Qt.AlignCenter)

        # Button signal setup
        [
            signal.connect(slot)
            for signal, slot in [
                (self.color_button.clicked, self.get_color),
                (self.region_button.clicked, self.collect_region),
                (self.aimbot_button.clicked, self.start_aimbot),
            ]
        ]

        # Inner layout setup
        self.inner_layout = QHBoxLayout()
        self.x_label,self.x_offset_input = QLabel("X Offset:"),QSpinBox()
        self.Y_label,self.y_offset_input = QLabel("Y Offset:"),QSpinBox()
        self.Y_label.setAlignment(Qt.AlignCenter),self.x_label.setAlignment(Qt.AlignCenter)
        self.x_offset_input.setMinimum(-2147483648),self.x_offset_input.setMaximum(2147483647)
        self.y_offset_input.setMinimum(-2147483648),self.y_offset_input.setMaximum(2147483647)

        [
            self.inner_layout.addWidget(widget)
            for widget in [
                (self.x_label),
                (self.x_offset_input),
                (self.Y_label),
                (self.y_offset_input)
            ]
        ]

        # Handles spinbox changes
        def offset(typ=None):
            print('kew')
            if typ == 'y': self.y_offset = self.y_offset_input.value()
            else: self.x_offset = self.x_offset_input.value()

        self.x_offset_input.valueChanged.connect(offset),self.y_offset_input.valueChanged.connect(lambda: offset('y'))

        # layout setup
        [
            layout.addWidget(*widget)
            for widget in [
                (self.region_label, 0, 1, 1, 1),
                (self.color_label, 0, 0, 1, 1),
                (self.color_button, 2, 0, 1, 1),
                (self.region_button, 2, 1, 1, 1),
                (self.aimbot_button, 5, 0, 1, 2),
            ]
        ]
        layout.addLayout(self.inner_layout, 4, 0, 1, 2)
        central_widget.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__": main()
