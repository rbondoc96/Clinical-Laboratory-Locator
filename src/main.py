import sys
import time
import concurrent.futures

from PyQt5 import QtWidgets

# Frontend
from ui.gui import Ui_MainWindow

# Backend
from navs.labcorp import LabcorpSearch
from navs.quest import QuestSearch

start = time.perf_counter()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.init_logic()
MainWindow.show()

app.exec_()
