import re

from aqt import mw
from aqt.qt import *

import maindialog
import editor
import uibuilder as ub
import deckfunctions as df

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
        mw.connect(self.frm.webView, SIGNAL("linkClicked(QUrl)"), self.link_clicked)
        mw.connect(d, SIGNAL("rejected()"), self.on_close)
        d.show()
    
    def link_clicked(self, url):
        mw.progress.start()
        link = url.toString()
        print "Link was: " + link
        
        if link == "setup":
            df.prepare_collection()
        elif link == "clean":
            df.clean_up()
        elif link.startswith("clear"):
            self.handle_clear(link)
        elif link.startswith("create"):
            self.handle_create(link)
        elif link.startswith("open"):
            self.handle_open(link)
        else:
            pass
    
        # Redraw SuperStyler window on every click
        self.frm.webView.setHtml(ub.get_body())
        
        mw.reset() #update anki UI
        mw.progress.finish()

    def on_close(self):
        self.has_instance = False


    def handle_open(self, link):
        m = re.search("open note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        
        #----#----#
        server = df.get_open_server(model, tmpl)
        d = QDialog(mw)
        ed = editor.Dialog()
        ed.setupUi(mw, model, server, d)
        d.connect(d, SIGNAL("rejected()"), lambda: self.diag.setVisible(True))
    
        self.diag.setVisible(False)
        d.show()     
                   
    def handle_clear(self, link):
        m = re.search("clear note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        
        #----#----#
        # Empty the template
        tmpl = model['tmpls'][tmpl_ord]
        tmpl['qfmt'] = ''
        tmpl['afmt'] = ''
        mw.col.models.save(model, True)
        # But this doesn't delete the cards. Do that below.
        # Copied this from models.py -> remTemplate(). 
        
        cids = mw.col.db.list("""
    select c.id from cards c, notes f where c.nid=f.id and mid = ? and ord = ?""",
                                 model['id'], tmpl['ord'])
        
        mw.col.remCards(cids, notes=False)
        
        dyndeck = df.get_ss_dyndeck(model)
        if dyndeck is not None:
            mw.col.decks.rem(dyndeck['id'])
        
    def handle_create(self, link):
        m = re.search("create note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        
        #----#----#
        df.start_template_server(model, tmpl)
        print "MODEL: %s   ---  TMPL: %s  " % (model['name'], tmpl['name'])
                
    