# -*- coding: utf8 -*- 
# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# QScintilla editor to edit the stylesheet.
#
# QScintilla code is from:
# http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt/
# With minor modifications. 

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerCSS
        
class CSSEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(CSSEditor, self).__init__(parent)

        self.setUtf8(True)
        
        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Use 4 spaces instead of tabs
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        
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

        # not too small
        self.setMinimumSize(600, 450)
        
        # Allow horizontal scroll as line width increases
        self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTH, 5)
        self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)


    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)


if __name__ == "__main__":
    testcss = u"""
body
{
  background-color: #437;
}

/*Comment! Test some unicode...*/
body:hover:after
{
  content: "←←→→→→→→←←←←←←←"
}

#someid
{
  invalidthing: 53;
}

.someclass
{
  color: #222;
}
"""
    app = QApplication(sys.argv)
    editor = CSSEditor()
    editor.show()
    editor.setText(testcss)
    app.exec_()