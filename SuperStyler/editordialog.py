# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# The dialog that contains the text editor.

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dialog(QDialog):
        
    def setupUi(self, mw, editor, Dialog):
        self.mw = mw
        self.textEdit = editor
        Dialog.resize(550, 600)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        # Close button
        self.buttonClose = QDialogButtonBox(Dialog)
        self.buttonClose.setOrientation(Qt.Horizontal)
        self.buttonClose.setStandardButtons(QDialogButtonBox.Close)        
        self.connect(self.buttonClose, SIGNAL("accepted()"), Dialog.accept)
        self.connect(self.buttonClose, SIGNAL("rejected()"), Dialog.reject)
        self.buttonClose.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        QMetaObject.connectSlotsByName(Dialog)
    
