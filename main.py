import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

app = QApplication([])
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
