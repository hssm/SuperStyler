# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# Open the plugin dialog window and present a WebView to interact with
# the user. Interactions are handled as HTML anchor clicks.


import re

from aqt import mw
from aqt.qt import *

import maindialog
import editordialog
import uibuilder as ub
import deckfunctions as df
from csseditor import CSSEditor
import templateserver
        
class SuperStyler(object):
    
    has_instance = False    # Keep only 1 instance of the plugin window
    
    def show_dialog(self):
        if self.has_instance:
            return
        self.has_instance = True
        
        d = QDialog(mw)
        self.diag = d
        self.frm = maindialog.Ui_Dialog()
        self.frm.setupUi(d)
        self.frm.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.frm.webView.setHtml(ub.get_body())
        self.frm.webView.setStyleSheet(ub.get_stylesheet())
        mw.connect(self.frm.webView, SIGNAL("linkClicked(QUrl)"), self._link_clicked)
        mw.connect(d, SIGNAL("rejected()"), self._on_close)
        d.show()
    
    def _link_clicked(self, url):
        mw.progress.start()
        link = url.toString()
        
        if link == "setup":
            df.prepare_collection()
        elif link == "clean":
            df.clean_up()
        elif link.startswith("clear"):
            self._handle_clear(link)
        elif link.startswith("create"):
            self._handle_create(link)
        elif link.startswith("open"):
            self._handle_open(link)
        else:
            pass
    
        # Redraw SuperStyler and Anki windows on every click
        self._redraw()
        mw.progress.finish()

    def _on_close(self):
        self.has_instance = False

    def _handle_open(self, link):
        m = re.search("open note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        
        d = QDialog(mw)
        ed = editordialog.Dialog()
        css_ed = CSSEditor()
        css_ed.setText(model['css'])
        ed.setupUi(mw, css_ed, d)
        
        def on_change():
            model['css'] = css_ed.text()
            templateserver.update_stylesheet(model, model['css'])
        
        def on_close():
            mw.col.models.save(model)
            self.diag.setVisible(True)
            self._redraw()
                
        d.connect(css_ed, SIGNAL("textChanged()"), on_change)
        d.connect(d, SIGNAL("rejected()"), on_close)
        
        self.diag.setVisible(False)
        d.show()
        
    def _handle_clear(self, link):
        m = re.search("clear note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        
        # Delete the template and all its cards
        df.empty_tmpl_and_cards(model, tmpl)
        # And also any dyndecks we created for this template
        dyndeck = df.get_ss_dyndeck(model)
        if dyndeck is not None:
            mw.col.decks.rem(dyndeck['id'])
            
        # And unhost it from our template server
        templateserver.remove_template(model)
        
    def _handle_create(self, link):
        m = re.search("create note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        templateserver.add_template(model, tmpl)
        df.create_styler_dyndeck(model)

    def _redraw(self):
        self.frm.webView.setHtml(ub.get_body())        
        mw.reset() #update anki UI
                