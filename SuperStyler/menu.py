# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# Add a menu option to open the plugin window. 

from aqt import mw
from aqt.qt import *

from superstyler import SuperStyler

# create menu items
ss_diag = SuperStyler()
ss_menu = QAction("Super Styler", mw)
mw.connect(ss_menu, SIGNAL("triggered()"), ss_diag.show_dialog)
# and add it to the tools menu
mw.form.menuTools.addAction(ss_menu)
