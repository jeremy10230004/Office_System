# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_new_price.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_price(object):
    def setupUi(self, Dialog_price):
        Dialog_price.setObjectName("Dialog_price")
        Dialog_price.resize(427, 172)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        Dialog_price.setFont(font)
        self.label_new_price = QtWidgets.QLabel(Dialog_price)
        self.label_new_price.setGeometry(QtCore.QRect(60, 10, 321, 41))
        self.label_new_price.setObjectName("label_new_price")
        self.button_new_price = QtWidgets.QPushButton(Dialog_price)
        self.button_new_price.setGeometry(QtCore.QRect(160, 120, 111, 41))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(14)
        self.button_new_price.setFont(font)
        self.button_new_price.setObjectName("button_new_price")
        self.input_new_price = QtWidgets.QLineEdit(Dialog_price)
        self.input_new_price.setGeometry(QtCore.QRect(50, 60, 331, 41))
        self.input_new_price.setObjectName("input_new_price")

        self.retranslateUi(Dialog_price)
        QtCore.QMetaObject.connectSlotsByName(Dialog_price)

    def retranslateUi(self, Dialog_price):
        _translate = QtCore.QCoreApplication.translate
        Dialog_price.setWindowTitle(_translate("Dialog_price", "新增價格等級"))
        self.label_new_price.setText(_translate("Dialog_price", "請輸入要新增的價格等級 :"))
        self.button_new_price.setText(_translate("Dialog_price", "確認"))
