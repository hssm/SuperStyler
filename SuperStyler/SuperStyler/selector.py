# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'styleSelector.ui'
#
# Created: Sun Sep  9 21:26:23 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(349, 219)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 291, 92))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelDeckSelect = QtGui.QLabel(self.layoutWidget)
        self.labelDeckSelect.setStyleSheet(_fromUtf8(""))
        self.labelDeckSelect.setObjectName(_fromUtf8("labelDeckSelect"))
        self.verticalLayout.addWidget(self.labelDeckSelect)
        self.comboModelSelect = QtGui.QComboBox(self.layoutWidget)
        self.comboModelSelect.setObjectName(_fromUtf8("comboModelSelect"))
        self.verticalLayout.addWidget(self.comboModelSelect)
        self.labelModelSelect = QtGui.QLabel(self.layoutWidget)
        self.labelModelSelect.setObjectName(_fromUtf8("labelModelSelect"))
        self.verticalLayout.addWidget(self.labelModelSelect)
        self.comboTmplSelect = QtGui.QComboBox(self.layoutWidget)
        self.comboTmplSelect.setObjectName(_fromUtf8("comboTmplSelect"))
        self.verticalLayout.addWidget(self.comboTmplSelect)
        self.btnStart = QtGui.QPushButton(Dialog)
        self.btnStart.setGeometry(QtCore.QRect(180, 170, 61, 24))
        self.btnStart.setFlat(False)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setGeometry(QtCore.QRect(249, 170, 61, 24))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDeckSelect.setText(QtGui.QApplication.translate("Dialog", "Select a model:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelModelSelect.setText(QtGui.QApplication.translate("Dialog", "Select a template:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(QtGui.QApplication.translate("Dialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

