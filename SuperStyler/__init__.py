# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# For some reason, loading our local copy of QScinttilla fails on Windows on
# the first try with "SystemError: dynamic module not initialized properly".
# Here, we load it and ignore the error, so that it will work when
# we load it again later.

try:
    from PyQt4.Qsci import QsciScintilla, QsciLexerCSS
except ImportError:
    try:
        from qtLocal.Qsci import QsciScintilla, QsciLexerCSS
    except:
        pass