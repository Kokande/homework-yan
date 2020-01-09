import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QWidget
import sqlite3


class Coffee_App(QMainWindow):
    def __init__(self, red):
        super().__init__()
        self.red = red
        uic.loadUi("main.ui", self)
        self.cursor = sqlite3.connect("coffee.sqlite").cursor()
        self.initUI()

    def initUI(self):
        rows = self.cursor.execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(rows))
        for i in range(len(rows)):
            for k in range(7):
                self.tableWidget.setItem(i, k, QTableWidgetItem(str(rows[i][k])))

        self.button.clicked.connect(self.redactor_open)

    def redactor_open(self):
        self.red.show()

    def closeEvent(self, *args, **kwargs):
        self.red.close()


class Redactor(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("coffee.sqlite")
        self.curs = self.con.cursor()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.textEdits = [self.sort, self.frying, self.status,
                          self.taste, self.price, self.volume]
        self.initUI()

    def initUI(self):
        self.load_button.clicked.connect(self.load_info)

        self.redact_button.clicked.connect(self.redact_info)

        self.save_button.clicked.connect(self.save_info)

    def load_info(self):
        id_info = self.curs.execute("""SELECT * FROM coffee WHERE ID = ?""",
                                    (self.ID.value(),)).fetchone()
        if id_info is not None:
            for i in range(6):
                self.textEdits[i].setText(str(id_info[i + 1]))
        else:
            for i in self.textEdits:
                i.clear()

    def save_info(self):
        global ex
        if self.curs.execute("""SELECT 1 FROM coffee WHERE ID = ?""",
                             (self.ID.value(),)).fetchone() is None:
            id_ = self.ID.value()
        else:
            id_ = self.curs.execute("""SELECT MAX(ID) FROM coffee""").fetchone()[0] + 1
        self.curs.execute("""INSERT INTO coffee VALUES(?,?,?,?,
                             ?,?,?)""", (id_,) + tuple((i.toPlainText()
                          for i in self.textEdits)))
        self.con.commit()
        ex.initUI()
        self.close()

    def redact_info(self):
        new_info = tuple((i.toPlainText()for i in self.textEdits)) + (self.ID.value(),)
        self.curs.execute("""UPDATE coffee SET [sort] = ?, [frying degree] = ?, 
                             [ground/beans] = ?, [taste description] = ?, [price] = ?, 
                             [volume of the pack] = ? WHERE ID = ?""", new_info)
        self.con.commit()
        ex.initUI()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    red = Redactor()
    ex = Coffee_App(red)
    ex.show()
    sys.exit(app.exec())
