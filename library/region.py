import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QDialog, QWidget
from PyQt5.QtCore import Qt

class PositionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Region")
        self.setGeometry(200, 200, 300, 200)
        self.setStyleSheet('background-color: black;')
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

class GetRegion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        self.setWindowTitle("Get Region")
        self.setFixedSize(250,100)
        self.setStyleSheet('background-color: rgb(30,30,30); color: white;')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Region: (0, 0) to (0, 0)")
        layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('font-family: Ubuntu; font-weight: bold;')

        self.dialog = PositionDialog()
        self.dialog.show()

        button = QPushButton("Get Dialog Region")
        button.clicked.connect(self.update_label)
        layout.addWidget(button)
        button.setStyleSheet('border-radius: 2px; background-color: rgb(50,50,50); padding: 3px; border: 1px solid white;')

        central_widget.setLayout(layout)

    def update_label(self):
        top_left, bottom_right = self.dialog.get_region()
        region_text = f"Region: ({top_left[0]}, {top_left[1]}) to ({bottom_right[0]}, {bottom_right[1]})"
        self.label.setText(region_text)

def main():
    app = QApplication(sys.argv)
    window = GetRegion()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__": main()
