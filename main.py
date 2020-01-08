import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sqlite3


class Coffee_App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.cursor = sqlite3.connect("coffee.sqlite").cursor()
        self.initUI()

    def initUI(self):
        rows = self.cursor.execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(rows))
        for i in range(len(rows)):
            for k in range(7):
                self.tableWidget.setItem(i, k, QTableWidgetItem(str(rows[i][k])))


if __name__ == '__main__':
    app = QApplication([])
    ex = Coffee_App()
    ex.show()
    sys.exit(app.exec())