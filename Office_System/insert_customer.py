from PyQt5 import QtWidgets
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

import ui_insert_customer as UI_main
import ui_new_country as UI_country
import ui_new_price as UI_price

import global_var as gv
import combo_choose
import item_function
import firestore_command as fc


class MainWindow(QtWidgets.QMainWindow):
    gv.init()

    def __init__(self, k):
        print(k)
        super(MainWindow, self).__init__()
        self.ui = UI_main.Ui_insert_actitvity()
        self.ui.setupUi(self)

        self.init_UI_combo()
        self.ui.label_error.hide()

        self.ui.button_insert.clicked.connect(self.input_data)
        self.ui.button_add_country.clicked.connect(self.new_country)
        self.ui.button_add_price.clicked.connect(self.new_price)
        self.ui.button_ff_find.clicked.connect(self.find_ff)

        self.ui.radiobutton_AL.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_TM.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_WA.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_WC.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_LN.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_EM.toggled.connect(lambda: self.init_UI_radio("software"))

        self.ui.radiobutton_first_yes.toggled.connect(lambda: self.init_UI_radio("first"))
        self.ui.radioButton_first_no.toggled.connect(lambda: self.init_UI_radio("first"))
        self.ui.radiobutton_custom_yes.toggled.connect(lambda: self.init_UI_radio("custom"))
        self.ui.radiobutton_custom_no.toggled.connect(lambda: self.init_UI_radio("custom"))

        self.ui.radiobutton_W.toggled.connect(lambda: self.init_UI_radio("package"))
        self.ui.radiobutton_W2.toggled.connect(lambda: self.init_UI_radio("package"))
        self.ui.radiobutton_B.toggled.connect(lambda: self.init_UI_radio("package"))
        self.ui.radiobutton_WB.toggled.connect(lambda: self.init_UI_radio("package"))

        self.ui.radiobutton_USD.toggled.connect(lambda: self.init_UI_radio("currency"))
        self.ui.radiobutton_RMB.toggled.connect(lambda: self.init_UI_radio("currency"))
        self.ui.radiobutton_help_yes.toggled.connect(lambda: self.init_UI_radio("help_pay"))
        self.ui.radioButton_help_no.toggled.connect(lambda: self.init_UI_radio("help_pay"))

        self.ui.radiobutton_direct_yes.toggled.connect(lambda: self.init_UI_radio("direct"))
        self.ui.radiobutton_direct_no.toggled.connect(lambda: self.init_UI_radio("direct"))
        self.ui.radiobutton_sample_yes.toggled.connect(lambda: self.init_UI_radio("sample"))
        self.ui.radiobutton_sample_no.toggled.connect(lambda: self.init_UI_radio("sample"))

        self.ui.radiobutton_AL_2.toggled.connect(lambda: self.init_UI_radio("software_ff"))
        self.ui.radiobutton_TM_2.toggled.connect(lambda: self.init_UI_radio("software_ff"))
        self.ui.radiobutton_WA_2.toggled.connect(lambda: self.init_UI_radio("software_ff"))
        self.ui.radiobutton_WC_2.toggled.connect(lambda: self.init_UI_radio("software_ff"))
        self.ui.radiobutton_LN_2.toggled.connect(lambda: self.init_UI_radio("software_ff"))
        self.ui.radiobutton_EM_2.toggled.connect(lambda: self.init_UI_radio("software_ff"))

    def init_UI_combo(self):
        self.ui.input_country.addItems(combo_choose.ic_country_get())
        self.ui.input_level.addItems(combo_choose.ic_level)
        self.ui.input_pay.addItems(combo_choose.ic_pay_way)

    def init_UI_radio(self, kind):
        ans = item_function.radio_choose(self)
        gv.radio_code[kind] = ans

    def new_country(self):
        dialog = Add_country(self)
        dialog.mySignal_country.connect(self.signal_country)
        dialog.exec_()

    def signal_country(self, signal):
        if signal != "":
            self.ui.input_country.setItemText(0, signal)

    def new_price(self):
        dialog = Add_price(self)
        dialog.mySignal_price.connect(self.signal_price)
        dialog.exec_()

    def signal_price(self, signal):
        if signal != "":
            self.ui.input_level.setItemText(0, signal)

    def find_ff(self):
        ans = fc.select_db("ff", "name", self.ui.input_ff_name.text())
        if ans != {}:
            self.ui.input_ff_phone.setText(ans["phone"])
            self.ui.input_ff_address.setText(ans["address"])
            item_function.radio_default([self.ui.radiobutton_help_yes, self.ui.radioButton_help_no], ans["help_pay"])
        else:
            self.ui.input_ff_phone.clear()
            self.ui.input_ff_address.clear()
            self.ui.radioButton_help_no.click()

    def input_data(self):
        if self.ui.input_name.text() == "":
            self.ui.label_error.show()
        else:
            reply = QMessageBox.question(self, "確認一下", "確定一下都沒有寫錯了嗎?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.ff_data = {
                    "name": self.ui.input_ff_name.text(),
                    "phone": self.ui.input_ff_phone.text(),
                    "address": self.ui.input_ff_address.text(),
                    "help_pay": gv.radio_code["help_pay"],
                    "remark": "",
                    "software": gv.radio_code["software_ff"],
                    "sf_id": self.ui.input_software_id_ff.text()
                }
                self.customer_data = {
                    "name": self.ui.input_name.text(),
                    "country": self.ui.input_country.currentText(),
                    "address": self.ui.input_address.text(),
                    "software": gv.radio_code["software"],
                    "sf_id": self.ui.input_software_id.text(),
                    "first": gv.radio_code["first"],
                    "custom": gv.radio_code["custom"],
                    "level": self.ui.input_level.currentText(),
                    "package": gv.radio_code["package"],
                    "phone": self.ui.input_phone.text(),
                    "pay_way": self.ui.input_pay.currentText(),
                    "currency": gv.radio_code["currency"],
                    "remark": self.ui.textEdit.toPlainText(),
                    "market": self.ui.input_market.text(),
                    "ff": self.ff_data["name"],
                    "ff_list": [self.ui.input_ff_name.text()],
                    "direct": gv.radio_code["direct"],
                    "sample": gv.radio_code["sample"]
                }

                fc.set_db("customer", self.customer_data["name"], self.customer_data)
                if self.ui.input_ff_name.text() != "":
                    fc.set_db("ff", self.ff_data["name"], self.ff_data)

                #print("Successfully insert!")
                gv.radio_code_clear(gv.radio_code)
                self.close()


class Add_country(QtWidgets.QDialog):
    mySignal_country = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Add_country, self).__init__(parent)
        self.ui = UI_country.Ui_Dialog_country()
        self.ui.setupUi(self)

        self.ui.button_new_country.clicked.connect(self.get_new_country)

    def get_new_country(self):
        self.data = self.ui.input_new_country.text()
        self.mySignal_country.emit(self.data)

        self.ui.input_new_country.clear()
        self.close()


class Add_price(QtWidgets.QDialog):
    mySignal_price = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Add_price, self).__init__(parent)
        self.ui = UI_price.Ui_Dialog_price()
        self.ui.setupUi(self)

        self.ui.button_new_price.clicked.connect(self.get_new_price)

    def get_new_price(self):
        self.data = self.ui.input_new_price.text()
        self.mySignal_price.emit(self.data)

        self.ui.input_new_price.clear()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
