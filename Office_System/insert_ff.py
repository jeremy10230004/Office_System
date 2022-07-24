from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import QMessageBox

import ui_insert_ff as UI_ff

import global_var as gv
import item_function
import firestore_command as fc


class MainWindow(QtWidgets.QMainWindow):
    gv.init()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UI_ff.Ui_insert_actitvity()
        self.ui.setupUi(self)

        self.ui.label_error.hide()

        self.ui.button_insert.clicked.connect(self.input_data)

        self.ui.radiobutton_AL.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_TM.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_WA.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_WC.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_LN.toggled.connect(lambda: self.init_UI_radio("software"))
        self.ui.radiobutton_EM.toggled.connect(lambda: self.init_UI_radio("software"))

        self.ui.radiobutton_help_yes.toggled.connect(lambda: self.init_UI_radio("help_pay"))
        self.ui.radioButton_help_no.toggled.connect(lambda: self.init_UI_radio("help_pay"))

    def init_UI_radio(self, kind):
        ans = item_function.radio_choose(self)
        gv.radio_code[kind] = ans

    def input_data(self):
        if self.ui.input_ff_name.text() == "":
            self.ui.label_error.show()
        else:
            reply = QMessageBox.question(self, "確認一下", "確定一下都沒有寫錯了嗎?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.ff_data = {
                    "name": self.ui.input_ff_name.text(),
                    "phone": self.ui.input_ff_phone.text(),
                    "address": self.ui.input_ff_address.text(),
                    "software": gv.radio_code["software"],
                    "help_pay": gv.radio_code["help_pay"],
                    "remark": "",
                    "sf_id": self.ui.input_software_id.text()
                }

                fc.set_db("ff", self.ff_data["name"], self.ff_data)

                # print("Successfully insert!")
                gv.radio_code_clear(gv.radio_code)
                self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
