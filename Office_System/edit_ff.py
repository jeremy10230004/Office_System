from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import QMessageBox

import ui_insert_ff as UI_ff

import global_var as gv
import item_function
import firestore_command as fc


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UI_ff.Ui_insert_actitvity()
        self.ui.setupUi(self)

        self.ui.label_error.hide()

        self.ui.button_insert.clicked.connect(self.input_data)

        self.radio_code = {"help_pay": "否"}

        self.ui.radiobutton_help_yes.toggled.connect(lambda: self.init_UI_radio("help_pay"))
        self.ui.radioButton_help_no.toggled.connect(lambda: self.init_UI_radio("help_pay"))

        self.default_data()

    def default_data(self):
        key = gv.get_value('edit_ff_default')
        data_dict_ff = fc.get_db('ff', key)

        if data_dict_ff['help_pay'] == '是':
            self.ui.radiobutton_help_yes.click()
        elif data_dict_ff['help_pay'] == '否':
            self.ui.radioButton_help_no.click()

        self.ui.input_ff_name.setText(data_dict_ff['name'])
        self.ui.input_ff_phone.setText(data_dict_ff['phone'])
        self.ui.input_ff_address.setText(data_dict_ff['address'])

    def init_UI_radio(self, kind):
        ans = item_function.radio_choose(self)
        self.radio_code[kind] = ans

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
                    "help_pay": self.radio_code["help_pay"],
                    "remark": "",
                    "sf_id": self.ui.input_software_id_ff.text()
                }

                fc.set_db("ff", self.ff_data["name"], self.ff_data)

                #print("Successfully insert!")
                self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
