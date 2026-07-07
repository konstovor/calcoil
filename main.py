import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_main import *
from PyQt5.QtGui import QFont
import database
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_connects()
        self.db = database.DatabaseManager()
        self.db.init_db()
        self.refresh_table()

    def set_connects(self):
        self.ui.dist_dspinb.valueChanged.connect(self.upd_cons)
        self.ui.liters_dspinb.valueChanged.connect(self.upd_cons)
        self.ui.liters_dspinb.valueChanged.connect(self.upd_cost)
        self.ui.price_dspinb.valueChanged.connect(self.upd_cost)
        self.ui.sav_btn.clicked.connect(self.adde)
        self.ui.chang_btn.clicked.connect(self.edite)
        self.ui.delet_btn.clicked.connect(self.deletee)
        self.ui.do_imag_btn.clicked.connect(self.do_imagee)
        self.ui.table.itemSelectionChanged.connect(self.select_rowe)
        self.ui.cleare.clicked.connect(self.clear_fields)

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

    def adde(self):
        if self.ui.dist_dspinb.value() == 0 or self.ui.liters_dspinb.value() == 0:
            QtWidgets.QMessageBox.warning(self, "Ошибка валидации", "Поля 'Дистанция(км)' и 'Литры' обязательны для заполнения.")
            self.ui.dist_dspinb.setFocus()
            self.ui.liters_dspinb.setFocus()
            return
        data = {
            "distance": self.ui.dist_dspinb.value(),
            "liters": self.ui.liters_dspinb.value(),
            "price": self.ui.price_dspinb.value(),
            "consumption": self.ui.cons_lineE.text().strip(),
            "cost": self.ui.cost_lineE.text().strip()
        }
        self.db.insert_record(data)
        self.refresh_table()
        self.clear_fields()
        QtWidgets.QMessageBox.information(self, "Успех", "Запись добавлена в базу.")

    def edite(self):
        selected = self.ui.table.selectionModel().selectedRows()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Выберите запись в таблице.")
            return
        row = selected[0].row()
        item_id = self.ui.table.item(row, 0).data(Qt.UserRole)
        if self.ui.dist_dspinb.value() == 0 or self.ui.liters_dspinb.value() == 0:
            QtWidgets.QMessageBox.warning(self, "Ошибка валидации", "Поля 'Дистанция(км)' и 'Литры' обязательны для заполнения.")
            self.ui.dist_dspinb.setFocus()
            self.ui.liters_dspinb.setFocus()
            return
        data = {
            "id": item_id,
            "distance": self.ui.dist_dspinb.value(),
            "liters": self.ui.liters_dspinb.value(),
            "price": self.ui.price_dspinb.value(),
            "consumption": self.ui.cons_lineE.text().strip(),
            "cost": self.ui.cost_lineE.text().strip()
        }
        self.db.update_record(data)
        self.refresh_table()
        QtWidgets.QMessageBox.information(self, "Успех", "Запись обновлена.")

    def deletee(self):
        selected = self.ui.table.selectionModel().selectedRows()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Выберите запись для удаления.")
            return
        if QtWidgets.QMessageBox.question(self, "Подтверждение", "Удалить выбранную запись?") == QtWidgets.QMessageBox.Yes:
            row = selected[0].row()
            item_id = self.ui.table.item(row, 0).data(Qt.UserRole)
            self.db.delete_record(item_id)
            self.refresh_table()
            self.clear_fields()

    def do_imagee(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        try:
            img = Image.open(path).convert("RGBA")
            img.thumbnail((260, 260), Image.LANCZOS)
            qt_img = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qt_img)
            self.ui.imag_lab.setPixmap(pixmap)
            self.ui.imag_lab.setStyleSheet("background-color: #fff; border: 2pxsolid #999; border-radius: 8px;")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение:\n{e}")


    def select_rowe(self):
        selected = self.ui.table.selectionModel().selectedRows()
        if not selected:
            self.clear_fields()
            return
        row = selected[0].row()
        self.ui.dist_dspinb.setValue(float(self.ui.table.item(row, 0).text()))
        self.ui.liters_dspinb.setValue(float(self.ui.table.item(row, 1).text()))
        self.ui.price_dspinb.setValue(float(self.ui.table.item(row, 2).text()))
            
            # Обновляем вычисляемые поля
        self.upd_cons()
        self.upd_cost()
            
            # Обновляем вычисляемые поля
        self.upd_cons()
        self.upd_cost()
        self.ui.cons_lineE.setText(str(self.ui.table.item(row, 3).text()))
        self.ui.cost_lineE.setText(str(self.ui.table.item(row, 4).text()))

    def clear_fields(self):
        self.ui.dist_dspinb.setValue(0.0)
        self.ui.liters_dspinb.setValue(0.0)
        self.ui.price_dspinb.setValue(0.0)
        self.ui.cons_lineE.setText(str(0.0))
        self.ui.cost_lineE.setText(str(0.0))
        self.ui.imag_lab.setText("Фото")
        self.ui.imag_lab.setStyleSheet("background-color: #f5f5f5; border: 2pxdashed #bbb; border-radius: 8px;")

    def refresh_table(self):
        self.ui.table.setRowCount(0)
        records = self.db.get_all()
        for i, rec in enumerate(records):
            self.ui.table.insertRow(i)
            self.ui.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(rec["distance"])))
            self.ui.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(rec["liters"])))
            self.ui.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(rec["price"] if rec["price"] is not None else "")))
            self.ui.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(rec["consumption"] if rec["consumption"] is not None else "")))
            self.ui.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(rec["cost"] if rec["cost"] is not None else "")))
            self.ui.table.item(i, 0).setData(Qt.UserRole, rec["id"])

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, "Выход", "Сохранить изменения перед выходом?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        elif reply == QtWidgets.QMessageBox.No:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())