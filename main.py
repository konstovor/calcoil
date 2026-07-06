import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_main import *
from PyQt5.QtGui import QFont


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_connects()
        self.upd_cons()
        self.upd_cost()

    def set_connects(self):
        self.ui.dist_dspinb.valueChanged.connect(self.upd_cons)
        self.ui.liters_dspinb.valueChanged.connect(self.upd_cons)
        self.ui.liters_dspinb.valueChanged.connect(self.upd_cost)
        self.ui.price_dspinb.valueChanged.connect(self.upd_cost)

    def upd_cons(self):
        dist = self.ui.dist_dspinb.value()
        liters = self.ui.liters_dspinb.value()
        if dist > 0:
            cons = (liters / dist) * 100
            self.ui.cons_lineE.setText(str(round(cons, 2)))
        else:
            self.ui.cons_lineE.setText("0.00")

    def upd_cost(self):
        liters = self.ui.liters_dspinb.value()
        price = self.ui.price_dspinb.value()
        cost = liters * price
        self.ui.cost_lineE.setText(str(round(cost, 2)))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())