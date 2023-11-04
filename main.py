import sys
import pyautogui
import threading
from library.AutoAimTrainer import AimTrainer as AutoAimTrainer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
    QColorDialog,
    QDialog,
)
from PyQt5.QtCore import Qt


class PositionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Region")
        self.setGeometry(200, 200, 300, 200)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.4)

    def get_region(self):
        window_pos = self.pos()
        window_width = self.width()
        window_height = self.height()

        top_left_x = window_pos.x()
        top_left_y = window_pos.y()
        bottom_right_x = top_left_x + window_width
        bottom_right_y = top_left_y + window_height
        return [top_left_x, top_left_y], [bottom_right_x, bottom_right_y]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.open,self.aimbot_active = False, False
        self.thread,self.color = None, None
        self.pos_dialog = PositionDialog()
        self.top_left, self.bottom_right = [0, 0], [0, 0]
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
        self.setFixedSize(350, 100)
        self.setStyleSheet(
            """
        QMainWindow{
            background-color: #6c6c6c;
        }
        QLabel{
            border-radius: 2px;
            background-color:#474747;
            color: white;
            border: 1px solid white;
        }
        QPushButton{
            border-radius: 2px;
            border: 1px solid black;
            padding: 2px;
            background-color: #e6e6e6;
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

        # Signal setup
        [
            signal.connect(slot)
            for signal, slot in [
                (self.color_button.clicked, self.get_color),
                (self.region_button.clicked, self.collect_region),
                (self.aimbot_button.clicked, self.start_aimbot),
            ]
        ]

        # layout setup
        [
            layout.addWidget(*widget)
            for widget in [
                (self.region_label, 0, 1, 1, 1),
                (self.color_label, 0, 0, 1, 1),
                (self.color_button, 2, 0, 1, 1),
                (self.region_button, 2, 1, 1, 1),
                (self.aimbot_button, 3, 0, 1, 2),
            ]
        ]
        central_widget.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__": main()
