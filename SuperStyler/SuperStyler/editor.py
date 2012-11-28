# From http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt/
# With minor modifications. 

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla, QsciLexerCSS

class Dialog(QDialog):
        
    def setupUi(self, mw, model, server, Dialog):
        self.mw = mw
        self.model = model
        self.textEdit = CSSEditor(server)
        self.textEdit.setText(model['css'])
        
        Dialog.resize(550, 600)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
                
        # Save button
        self.buttonSave = QDialogButtonBox(Dialog)
        self.buttonSave.setOrientation(Qt.Horizontal)
        self.buttonSave.setStandardButtons(QDialogButtonBox.Save)
        self.connect(self.buttonSave, SIGNAL("accepted()"), lambda: self.save_stylesheet())
        self.connect(self.buttonSave, SIGNAL("rejected()"), lambda: self.save_stylesheet())      

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
        self.horizontalLayout.addWidget(self.buttonSave)
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        QMetaObject.connectSlotsByName(Dialog)
    
    def save_stylesheet(self):
        self.model['css'] = self.textEdit.text()
        self.mw.col.models.save(self.model)
        
class CSSEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, server, parent=None):
        super(CSSEditor, self).__init__(parent)
        
        self.server = server
                
        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.connect(self,
            SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
            self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),
            self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set CSS lexer
        # Set style for CSS comments (style number 1) to a fixed-width
        # courier.
        #
        lexer = QsciLexerCSS()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(600, 450)
        
        self.connect(self, SIGNAL("textChanged()"), self.update_server)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def update_server(self):
        self.server.set_CSS(self.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CSSEditor(None)
    editor.show()
    editor.setText("body { background-color: #fff; }")
    app.exec_()