import pyperclip
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QCompleter
import ui_customer_main as UI

import global_var as gv
import combo_choose
import firestore_command as fc
import item_function

import insert_customer
import insert_ff
import edit_customer
import edit_ff
import excel_workspace

import sys
import datetime


class MainWindow(QtWidgets.QMainWindow):
    gv.init()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UI.Ui_search_window()
        self.ui.setupUi(self)

        self.init_UI_combo()
        self.ui.Button_customer_search.clicked.connect(self.search_customer)
        self.ui.Button_ff_search.clicked.connect(self.search_ff)

        self.ui.Button_customer_add.clicked.connect(self.to_insert_customer)
        self.ui.Button_ff_add.clicked.connect(self.to_insert_ff)
        self.ui.Button_customer_edit.clicked.connect(self.to_edit_customer)
        self.ui.Button_ff_edit.clicked.connect(self.to_edit_ff)
        self.ui.Button_customer_delete.clicked.connect(self.to_delete_customer)
        self.ui.Button_ff_delete.clicked.connect(self.to_delete_ff)

        self.ui.Button_paper.clicked.connect(self.remark_btn)
        self.ui.Button_copy_ff.clicked.connect(self.copy_ff)

        self.ui.list_customer.clicked.connect(self.table_click_customer)
        self.ui.list_ff.clicked.connect(self.table_click_ff)

        self.position = ''
        self.order_init_()
        self.todo_init_()

    def init_UI_combo(self):
        self.ui.comboBox_customer_search.addItems(combo_choose.cm_search_customer)
        self.ui.comboBox_ff_search_.addItems(combo_choose.cm_search_ff)

    def remark_update(self, p):
        if p == 'customer':
            fc.set_db(p, self.ui.table_data.item(0, 1).text(), {"remark": self.ui.textEdit_paper.toPlainText()}, True)
        elif p == 'ff':
            fc.set_db(p, self.ui.table_data.item(0, 1).text(), {"remark": self.ui.textEdit_paper.toPlainText()}, True)
        elif p == 'order':
            fc.set_db('customer', self.ui.order_list_customer.selectedItems()[0].text(),
                      {"order_remark": self.ui.order_remark.toPlainText()}, True)

    def search_customer(self):
        key = self.ui.comboBox_customer_search.currentText()
        title = gv.search_customer_title_list[key]
        if key == '未成交':
            ans_list = fc.select_all_db("customer", gv.search_customer_key[key], '否')
        elif key == '已寄樣品':
            ans_list = fc.select_all_db("customer", gv.search_customer_key[key], '已寄樣品')
        else:
            ans_list = fc.select_all_db("customer", gv.search_customer_key[key], self.ui.search_customer.text())
        if gv.search_customer_key[key] == "name":
            ans = item_function.table_data_choose(["name", "country"], ans_list)
        else:
            ans = item_function.table_data_choose(["name", gv.search_customer_key[key]], ans_list)
        item_function.table_show(self.ui.list_customer, title, ans)

    def search_ff(self):
        key = self.ui.comboBox_ff_search_.currentText()
        title = gv.search_ff_title_list[key]

        if gv.search_ff_key[key] == "name":
            ans_list = fc.select_all_db("ff", gv.search_ff_key[key], self.ui.search_ff.text())
            ans = item_function.table_data_choose(["name", "phone"], ans_list)

        elif gv.search_ff_key[key] == "country":
            cuss = fc.select_all_db('customer', 'country', self.ui.search_ff.text())
            ffs = []
            ans = []
            for cus in cuss:
                if cus['ff'] not in ffs:
                    ffs.append(cus["ff"])
                    ans.append([cus['ff'], cus['country']])

        elif gv.search_ff_key[key] == "customer":
            ans_dict = fc.select_all_db("customer", 'name', self.ui.search_ff.text())
            ans = []
            for person in ans_dict:
                for ff in person['ff_list']:
                    if ff != "":
                        ans.append([ff, person['name']])

        else:
            ans = [["出現錯誤", "出現錯誤"]]

        item_function.table_show(self.ui.list_ff, title, ans)

    def to_insert_customer(self):
        self.add_customer_window = insert_customer.MainWindow(2)
        self.add_customer_window.show()

    def to_insert_ff(self):
        self.add_ff_window = insert_ff.MainWindow()
        self.add_ff_window.show()

    def to_edit_customer(self):
        try:
            gv.set_value('edit_customer_default', self.ui.list_customer.selectedItems()[0].text())
            self.edit_customer_window = edit_customer.MainWindow()
            self.edit_customer_window.show()
        except:
            pass

    def to_edit_ff(self):
        try:
            gv.set_value('edit_ff_default', self.ui.list_ff.selectedItems()[0].text())
            self.edit_ff_window = edit_ff.MainWindow()
            self.edit_ff_window.show()
        except:
            pass

    def to_delete_customer(self):
        try:
            key = self.ui.list_customer.selectedItems()[0].text()
            if key != '':
                reply = QMessageBox.question(self, "確認一下", "確定要刪除嗎?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    fc.delete_db('customer', key)
                    self.search_customer()
                    self.ui.textEdit_paper.clear()
                    self.ui.table_data.clear()
                    self.position = ''
        except:
            pass

    def to_delete_ff(self):
        try:
            key = self.ui.list_ff.selectedItems()[0].text()
            if key != '':
                reply = QMessageBox.question(self, "確認一下", "確定要刪除嗎?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    all_list = fc.select_all_db('customer', "name", "")
                    for a in all_list:
                        fc.delete_list_contain('customer', a['name'], 'ff_list', key)
                    fc.delete_db('ff', key)
                    self.search_ff()
                    self.ui.textEdit_paper.clear()
                    self.ui.table_data.clear()
                    self.position = ''
        except:
            pass

    def remark_btn(self):
        self.remark_update(self.position)

    def table_click_customer(self):
        self.ui.textEdit_paper.clear()
        self.ui.table_data.clear()
        self.position = 'customer'

        person = self.ui.list_customer.selectedItems()[0].text()
        data_dict = fc.get_db("customer", person)
        data_dict_ff = fc.get_db("ff", data_dict["ff"])

        attributes = []
        for label in gv.label_key:
            attributes.append(data_dict[label])
        for label2 in gv.label_key_ff:
            if label2 not in data_dict_ff:  # 可能會沒有貨代
                attributes.append("")
            else:
                attributes.append(data_dict_ff[label2])

        i = 0

        for label in gv.table_data_customer:
            if i > len(attributes) - 1:
                gv.table_data_customer[label] = ""
            else:
                gv.table_data_customer[label] = attributes[i]
            i = i + 1

        item_function.data_table_show(self.ui.table_data, 'customer')
        self.ui.textEdit_paper.setText(data_dict["remark"])

        self.ui.table_data.resizeRowsToContents()
        gv.dict_clear(gv.table_data_customer)

    def table_click_ff(self):
        self.ui.textEdit_paper.clear()
        self.ui.table_data.clear()
        self.position = 'ff'

        person = self.ui.list_ff.selectedItems()[0].text()
        data_dict_ff = fc.get_db("ff", person)

        attributes = []
        for label2 in gv.label_key_ff:
            attributes.append(data_dict_ff[label2])
        i = 0
        for label in gv.table_data_ff:
            gv.table_data_ff[label] = attributes[i]
            i = i + 1

        item_function.data_table_show(self.ui.table_data, 'ff')
        self.ui.textEdit_paper.setText(data_dict_ff["remark"])

        self.ui.table_data.resizeRowsToContents()
        gv.dict_clear(gv.table_data_ff)

    def copy_ff(self):
        if self.position == 'customer':
            ff_data = "Name: %s\nPhone: %s\nAddress: %s" % \
                      (self.ui.table_data.item(13, 1).text(),
                       self.ui.table_data.item(14, 1).text(),
                       self.ui.table_data.item(15, 1).text())
        else:
            ff_data = "Name: %s\nPhone: %s\nAddress: %s" % \
                      (self.ui.table_data.item(0, 1).text(),
                       self.ui.table_data.item(1, 1).text(),
                       self.ui.table_data.item(2, 1).text())
        pyperclip.copy(ff_data)

    # ------------------------------------------------------------
    def order_init_(self):
        self.sizes = 0
        self.price_r = 0
        self.price_c = 0
        self.code = []
        self.code_lock = False
        self.sl_list = []
        self.ui.Button_check_code.clicked.connect(self.get_order_info)
        self.ui.Button_write_price.clicked.connect(self.set_price)
        self.ui.Button_write_code.clicked.connect(self.set_all_order)
        self.ui.Button_customer_search_2.clicked.connect(self.order_search_customer)
        self.ui.order_list_customer.clicked.connect(self.order_search_clicked)
        self.ui.Button_push_remark.clicked.connect(self.order_remark_btn)
        self.ui.Button_tran_order.clicked.connect(self.order_tran)

    def get_order_info(self):
        self.code = []
        try:
            self.sizes = [self.ui.size_range_1.text(), self.ui.size_range_2.text(), self.ui.size_range_3.text()]
            while "" in self.sizes:
                self.sizes.remove("")
            self.sl_list = [self.ui.order_SL_1.text(), self.ui.order_SL_2.text(), self.ui.order_SL_3.text()]
            while "" in self.sl_list:
                self.sl_list.remove("")
            self.spread_list = [0, self.ui.order_spread_1.text(), self.ui.order_spread_2.text()]
            while "" in self.spread_list:
                self.spread_list.remove("")
            if len(self.spread_list) == 3:
                self.spread_list[2] = float(self.spread_list[1]) + float(self.spread_list[2])
            if len(self.spread_list) != len(self.sl_list):
                return 0

            self.price_c = len(self.sizes)
            self.price_r = int(self.ui.order_code_end.text()) - int(self.ui.order_code_start.text())

            for sl in self.sl_list:
                temp = []
                for i in range(int(self.ui.order_code_start.text()), int(self.ui.order_code_end.text()) + 1):
                    if i < 1000:
                        temp.append(f"{self.ui.order_code_title.text()}0{i}{sl}")
                    else:
                        temp.append(f"{self.ui.order_code_title.text()}{i}{sl}")
                self.code.append(temp)

            self.code_lock = True
            self.ui.order_error.setText(f"已確認產品資訊")
            gv.set_value("order_img_check", 0)
        except:
            self.show_error_order("尺碼段或產品編號出錯")

    def set_bar(self):
        excel_workspace.input_bar(self.sizes)

    def set_price(self):
        if not self.code_lock:
            self.show_error_order("先確認產品資訊")
            return 0
        else:
            self.ui.order_error.setText("LOADING...")

        # 生成空價格表
        if self.price_r != 0:
            err = excel_workspace.edit_price_file(self.sizes, self.code)

            self.ui.order_error.setText("價格表建立完成")
            if err != "":
                self.show_error_order(err)

        else:
            self.show_error_order("產品編號出錯")

    def set_all_order(self):
        for sl_num in range(len(self.sl_list)):
            self.set_bar()
            self.set_order(sl_num)

    def set_order(self, sl_num):
        self.ui.order_error.clear()
        if not self.code_lock:
            self.show_error_order("先確認產品資訊")
            return 0
        else:
            if self.ui.exchange_rate.text() == "":
                self.show_error_order("請輸入匯率")
                return 0
            else:
                self.ui.order_error.setText(f"LOADING...")
        if gv.get_value("order_img_check") == 0:
            gv.set_value("order_img_check", 0)
        # 加入編號
        excel_workspace.input_code(self.code[sl_num])
        # 刪除多餘列(30)
        excel_workspace.hide_col(self.price_r)
        # 加入info
        self.info_list = [self.ui.order_code_info_1.text(), self.ui.order_code_info_2.text(),
                          self.ui.order_code_info_3.text(),
                          self.ui.order_code_info_4.text(), self.ui.order_code_info_5.text()]
        excel_workspace.input_info(self.info_list)
        # 遷入購買規則
        excel_workspace.input_rule(self.ui.order_rules.toPlainText())
        # 取出價格表的價格，然後導入
        price_list = excel_workspace.get_price()

        # 加入函式
        excel_workspace.input_function(self.sizes, self.price_c, self.price_r)
        # 縮小圖片
        # 加入圖片
        try:
            excel_workspace.make_img_small(self.ui.series.text(), self.code[sl_num])
            excel_workspace.input_img(self.price_r, self.ui.series.text(), self.code[sl_num])
        except:
            self.show_error_order("圖片部份發生錯誤")
            gv.set_value("order_img_check", 1)
            return 0
        # 設定不同訂價
        excel_workspace.input_price(price_list, float(self.spread_list[sl_num]), float(self.ui.exchange_rate.text()),
                                    self.ui.series.text(), self.sl_list[sl_num])

        if gv.get_value("order_img_check") == 0:
            self.ui.order_error.setText("~~訂單生成完畢~~")
        else:
            self.show_error_order("圖片部份發生錯誤")
        return 0

    def show_error_order(self, text):
        self.ui.order_error.setText(f"**<ERROR>** : {text}")

    def order_search_customer(self):
        key = "name"
        ans_list = fc.select_all_db("customer", key, self.ui.order_search_customer.text())
        ans = item_function.table_data_choose([key, "country"], ans_list)
        item_function.table_show(self.ui.order_list_customer, [key, "country"], ans)

    def order_search_clicked(self):
        self.position = 'customer'
        self.ui.order_remark.clear()
        person = self.ui.order_list_customer.selectedItems()[0].text()

        data_dict = fc.get_db("customer", person)
        if "order_remark" in data_dict:
            self.ui.order_remark.setText(data_dict["order_remark"])

    def order_remark_btn(self):
        self.remark_update("order")

    def order_tran(self):
        sl_kind = excel_workspace.tran_choose_original(self.ui.order_tran_path.text())
        # 基礎設定
        code_list, size_list = excel_workspace.tran_set_code(self.ui.order_tran_path.text(), sl_kind)
        # 圖片
        excel_workspace.tran_set_img(code_list, self.ui.order_tran_path.text())
        # 數字
        excel_workspace.tran_put_lot(self.ui.order_tran_path.text(), code_list, size_list)
        # 名字
        # remark

    # ------------------------------------------------------------
    # ------------------------------------------------------------
    def todo_init_(self):
        self.todo_ID = ""
        self.todo_key = ""
        self.ui.todo_date.setText(self.set_today())

        self.ui.Button_todo_empty.clicked.connect(self.todo_empty)
        self.ui.Button_todo_input.clicked.connect(self.todo_input)
        self.ui.Button_todo_update.clicked.connect(self.todo_update)
        self.ui.Button_todo_delete.clicked.connect(self.todo_delete)
        self.ui.Button_todo_login.clicked.connect(self.todo_login)
        self.ui.Button_todo_search.clicked.connect(self.todo_search)
        self.ui.table_todo.clicked.connect(self.todo_clicked)

        self.ui.todo_id.returnPressed.connect(self.todo_login)
        self.ui.todo_search.returnPressed.connect(self.todo_search)

        self.ui.todo_level.addItems(combo_choose.todo_level)
        self.ui.comboBox_todo_search.addItems(combo_choose.todo_serach + combo_choose.todo_level)

    def set_today(self):
        datetime.timezone(datetime.timedelta(hours=8))
        today = datetime.date.today()
        return f"{today.year}/{today.month}/{today.day}"

    def zero_type(self, old_date):
        if len(old_date.split("/")) != 3:
            self.ui.todo_error.setText("~日期錯誤~")
            self.ui.todo_date.clear()
            return ""
        y, m, d = old_date.split("/")
        if len(m) == 1:
            m = f"0{m}"
        if len(d) == 1:
            d = f"0{d}"

        return f"{y}/{m}/{d}"

    def todo_empty(self):
        self.ui.todo_date.setText(self.set_today())
        self.ui.todo_person.clear()
        self.ui.todo_content.clear()
        self.ui.todo_remark.clear()

    def todo_login(self):
        self.ui.todo_error.clear()
        if self.ui.todo_id.text() != "":
            ans = fc.get_db('user', self.ui.todo_id.text())
            if ans is not None:
                self.todo_ID = self.ui.todo_id.text()
                completer = QCompleter(fc.find_all_db(f"{self.todo_ID}_todo", "person"))
                self.ui.todo_search.setCompleter(completer)
                self.todo_show()

    def todo_input(self):
        self.ui.todo_error.clear()
        if self.todo_ID == "":
            self.ui.todo_error.setText("~尚未登入~")
            return 0
        if self.ui.todo_date.text() == "":
            self.ui.todo_error.setText("~未輸入日期~")
            return 0
        date_list = self.ui.todo_date.text().split("/")
        if len(date_list) != 3:
            self.ui.todo_error.setText("~錯誤日期格式~")
            return 0
        if self.ui.todo_content.toPlainText() == "":
            self.ui.todo_error.setText("~未輸入事項內容~")
            return 0

        todo_dict = {
            "date": self.zero_type(self.ui.todo_date.text()),
            "level": self.ui.todo_level.currentText(),
            "content": self.ui.todo_content.toPlainText(),
            "person": self.ui.todo_person.text(),
            "remark": self.ui.todo_remark.toPlainText(),
        }
        fc.set_db(f"{self.todo_ID}_todo", todo_dict["content"], todo_dict)
        self.todo_show()
        self.todo_empty()

    def todo_update(self):
        if self.todo_key != "":
            reply = QMessageBox.question(self, "確認一下", f"確定要修改\n{self.todo_key}嗎?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                fc.delete_db(f'{self.todo_ID}_todo', self.todo_key)
                self.todo_input()
        self.todo_empty()

    def todo_show(self, input_list=None):
        if input_list is None:
            ans_list = fc.find_all_db(f"{self.todo_ID}_todo", "content", filter_same=False)
        else:
            ans_list = input_list

        ans = self.todo_sort(
            [[a_dict["date"], a_dict["level"], a_dict["person"], a_dict["content"], a_dict["remark"]]
             for a_dict in ans_list])
        item_function.table_show(self.ui.table_todo, ["日期", "緊急程度", "關係人名稱", "內容", "備註"], ans)
        self.ui.table_todo.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table_todo.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table_todo.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        self.ui.table_todo.setColumnWidth(2, 150)
        self.ui.table_todo.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        self.ui.table_todo.setColumnWidth(4, 225)

        for i in range(self.ui.table_todo.rowCount()):
            self.ui.table_todo.item(i, 4).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        for i in range(self.ui.table_todo.rowCount()):
            if self.ui.table_todo.item(i, 1).text() == combo_choose.todo_level[1]:
                self.ui.table_todo.item(i, 1).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            elif self.ui.table_todo.item(i, 1).text() == combo_choose.todo_level[-1]:
                self.ui.table_todo.item(i, 1).setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 255)))

        self.ui.table_todo.resizeRowsToContents()

    @staticmethod
    def todo_sort(input_list):
        if len(input_list) <= 1:
            return input_list

        step_1 = sorted(input_list, reverse=True)
        ans = []
        temp = [step_1[0]]
        level = [combo_choose.todo_level[1], combo_choose.todo_level[2], combo_choose.todo_level[0]]

        for i in range(1, len(step_1)):
            if step_1[i][0] == step_1[i - 1][0]:
                temp.append(step_1[i])
            else:
                for l in level:
                    for t in temp:
                        if t[1] == l:
                            ans.append(t)
                temp = [step_1[i]]
        for l in level:
            for t in temp:
                if t[1] == l:
                    ans.append(t)
        for finish in step_1:
            if finish[1] == combo_choose.todo_level[3]:
                ans.append(finish)

        # ------------------------------------

        return ans

    def todo_delete(self):

        self.ui.todo_error.clear()
        if self.todo_ID == "":
            self.ui.todo_error.setText("~尚未登入~")
            return 0
        try:
            keys = []
            print(len(self.ui.table_todo.selectedItems()))
            for i in range(len(self.ui.table_todo.selectedItems())):
                if i % 5 == 3:
                    keys.append(self.ui.table_todo.selectedItems()[i].text())
            reply = QMessageBox.question(self, "確認一下", "確定要刪除嗎?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                for key in keys:
                    if key != '':
                        fc.delete_db(f'{self.todo_ID}_todo', key)
                        self.todo_key = ""
                        self.search_customer()
            self.todo_show()
            self.todo_empty()
        except:
            print("刪除失敗")
            pass

    def todo_clicked(self):
        date = self.ui.table_todo.selectedItems()[0].text()
        level = self.ui.table_todo.selectedItems()[1].text()
        person = self.ui.table_todo.selectedItems()[2].text()
        content = self.ui.table_todo.selectedItems()[3].text()
        remark = self.ui.table_todo.selectedItems()[4].text()

        self.ui.todo_date.setText(date)
        self.ui.todo_level.setCurrentText(level)
        self.ui.todo_person.setText(person)
        self.ui.todo_content.setText(content)
        self.ui.todo_remark.setText(remark)

        self.todo_key = content

    def todo_search(self):
        self.ui.todo_error.clear()
        self.ui.table_todo.clear()

        if self.todo_ID == "":
            self.ui.todo_error.setText("~尚未登入~")
            return 0
        # ------------------------------
        key = self.ui.comboBox_todo_search.currentText()
        if key in combo_choose.todo_level:
            ans_list = fc.select_all_db(f"{self.todo_ID}_todo", "level", key)
        else:
            ans_list = fc.select_all_db(f"{self.todo_ID}_todo", gv.todo_key[key], self.ui.todo_search.text())
        self.todo_show(input_list=ans_list)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
