# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# Load the correct qscintilla library for the current platform.
#
# For some reason, when first loading our local copies of QScintilla, they 
# throw an error: "SystemError: dynamic module not initialized properly".
# However, the PyQt4.Qsci module is still loaded, so it will work when
# invoked later on. Here, we decide which library to use and simply
# ignore the error that comes along with it.

import sys
import platform


try:
    # We'll try using the natively installed one first, and fall back
    # on our local copy if it's not installed.
    import PyQt4.Qsci
except ImportError:
    try:
        if sys.platform.startswith('win'):
            import qtLocal.win.Qsci
        elif sys.platform.startswith('linux'):
            if platform.architecture()[0] == "64bit":
                import qtLocal.linux64.Qsci
            elif platform.architecture()[0] == "32bit":
                import qtLocal.linux32.Qsci
        else:
            pass
    except:
        pass