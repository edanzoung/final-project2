import sys
from PyQt6.QtWidgets import QApplication
from logic import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

sys.exit(app.exec())