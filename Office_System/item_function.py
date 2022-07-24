"""
def choose_software():
    radioBtn = self.sender()
    if radioBtn.isChecked():
        self.software_code = self.software[radioBtn.text()]
"""
from PyQt5 import QtWidgets
import global_var as gv


def radio_choose(class_):
    code = ""
    radioBtn = class_.sender()
    if radioBtn.isChecked():
        code = radioBtn.text()

    return code


def radio_default(item_list, ans):
    for item in item_list:
        if item.text() == ans:
            item.click()


def table_data_choose(rule, data_list):
    ans = []
    for a in data_list:
        person = []
        for r in rule:
            person.append(a[r])
        ans.append(person)

    return ans


def table_show(table, headerList, item_list):
    table.setRowCount(0)
    table.setColumnCount(len(headerList))
    table.setHorizontalHeaderLabels(headerList)

    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    for i in range(len(item_list)):
        item_list2 = item_list[i]
        row = table.rowCount()
        table.insertRow(row)
        for j in range(len(item_list2)):
            item = QtWidgets.QTableWidgetItem(str(item_list[i][j]))
            table.setItem(row, j, item)


# ------------------------------------4.0 ------------------------------------------
def data_table_show(table, position):

    if position == 'customer':
        data_dict = gv.table_data_customer
    else:
        data_dict = gv.table_data_ff
    table.setRowCount(0)  # init
    table.setColumnCount(2)
    table.verticalHeader().setVisible(False)  # 去掉垂直標頭
    table.horizontalHeader().setVisible(False)  # 去掉水平標頭
    table.horizontalHeader().setStretchLastSection(True)  # 末欄自動填滿
    table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    # https://blog.csdn.net/u011731378/article/details/80347778

    for i in data_dict:
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(i))
        table.setItem(row, 1, QtWidgets.QTableWidgetItem(data_dict[i]))
