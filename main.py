from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
import sys
from ui import Ui_MainWindow
from logic import applyLogic


app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
applyLogic(ui)
MainWindow.show()

app.exec()