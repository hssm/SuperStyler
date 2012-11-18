import time
import re

from aqt import mw
from aqt.qt import *
import dialog

import utils
import templateserver

PREFIX = '##Styler'

class SuperStyler(object):
    
    def show_dialog(self):
        d = QDialog(mw)
        self.frm = dialog.Ui_Dialog()
        self.frm.setupUi(d)
        self.frm.webView.page().setLinkDelegationPolicy(
                QWebPage.DelegateAllLinks)
        
        self.frm.webView.setHtml(self.get_body())
        self.frm.webView.setStyleSheet(self.get_stylesheet())
        mw.connect(self.frm.webView, SIGNAL("linkClicked(QUrl)"),
                   self.link_clicked)
        d.show()
    
    def get_body(self):
        if self.need_prepare():
            return self.get_prepare_body()
        else:
            body =\
"""
<table width=100%%>
<tr>
<th align=left>Note</th>
<th align=left>Card</th>
<th align=left>Server open</th>
<th align=left>Create server+deck</th>
</tr>
%s
</table>
<a href="clean">Clean up</a>
"""
            s = ''
            color1 = '#ccc'
            color2 = '#eee'
            
            for model in mw.col.models.all():
                s += self.get_model_row(model, color1)
                for tmpl in model['tmpls']:
                    if tmpl['name'].startswith(PREFIX):
                        continue
                    s += self.get_tmpl_row(model, tmpl, color1)
                (color1, color2) = (color2, color1)
            return body % s
                    
    
    def get_model_row(self, model, color):
        row =\
"""
<tr style="background-color:%s;">
<td>%s</td>
<td/>
<td/>
<td/>
""" % (color, model['name'])
        return row
    
    def get_tmpl_row(self, model, card, color):
        row =\
"""
<tr style="background-color:%s;">
<td/>
<td>%s</td>
<td/>
<td><a href="create note:'%s' card:'%s'">Create</a></td>
""" % (color, card['name'], model['id'], card['ord'])
        return row
    
    def get_prepare_body(self):
        return\
"""
<h1>Need to prepare collection</h1>
<br>
<a href="setup">Click here!</a>
<br>
<p>Explain what happens here!</p>
<a href="clean">Clean up</a>
""" 
    
    def get_stylesheet(self):
        return\
"""
<style>
table
{
  background-color: #437;
  color: #fff;
}
</style>
"""
          
        
    def link_clicked(self, url):
        mw.progress.start()
        link = url.toString()
        print "Link was: " + link
        if link == "setup":
            self.prepare_collection()
        elif link == "clean":
            self.clean_up()
        elif link.startswith("create"):
            m = re.search("create note:'(.+)' card:'(.+)'", link)
            model_id = m.group(1)
            tmpl_ord = int(m.group(2))
            model = mw.col.models.get(model_id)
            tmpl = model['tmpls'][tmpl_ord]
            self.start_template_server(model, tmpl)
            print "MODEL: %s   ---  TMPL: %s  " % (model['name'], tmpl['name'])            
        else:
            pass
        
        self.frm.webView.setHtml(self.get_body())
        mw.reset() #update anki UI
        mw.progress.finish()
        
    def need_prepare(self):
        """Check if the plugin needs to create a SuperStyler card type
        for any of the models. If any are missing it, return True."""
        
        for model in mw.col.models.all():
            if not self.has_ss_tmpl(model):
                return True
        return False
    
    def has_ss_tmpl(self, model):
        for tmpl in model['tmpls']:
            if tmpl['name'].startswith(PREFIX):
                return True
        return False
            
    def prepare_collection(self):
        print "Preparing collection...",
        mw.progress.start()
        for model in mw.col.models.all():
            if not (self.has_ss_tmpl(model)):
                tmpl_name = PREFIX + "-" + str(int(time.time()*1000))
                new_tmpl = mw.col.models.newTemplate(tmpl_name)
                new_tmpl['qfmt'] = ''
                new_tmpl['afmt'] = ''
                mw.col.models.addTemplate(model, new_tmpl)
                mw.col.models.save(model, True)
        print "Done!"
        mw.progress.finish()
        
    
    def start_template_server(self, model, tmpl):
        # Start a new template server on a free port
        port = utils.get_free_port()
        server = templateserver.start_new_server("0.0.0.0", port)
        
        # Read our script into memory
        scriptPath = os.path.join(os.path.dirname(__file__), 'script.js')
        script = open(scriptPath, 'r').read()
        
        # Update the script with our machine's local network IP and port
        url = str(utils.get_lan_ip()) + ':' + str(port)
        script = script.replace('##AddressGoesHere##', url)
                
        srv_tmpl = None
        # Get the styler template (or create it if it doesn't exist)
        for _tmpl in model['tmpls']:
            if _tmpl['name'].startswith(PREFIX):
                srv_tmpl = _tmpl
                break
            
        if not srv_tmpl:
            cardName = PREFIX + "-" + str(int(time.time()*1000))
            srv_tmpl = mw.col.models.newTemplate(cardName)
            # Add it to the model we selected
            mw.col.models.addTemplate(model, srv_tmpl)
            
        srv_tmpl['qfmt'] = script + tmpl['qfmt']
        srv_tmpl['afmt'] = script + tmpl['afmt']
        mw.col.models.save(model, True)
        
        self.create_styler_dyndeck(model, srv_tmpl, tmpl['name'])
        
    
    def create_styler_dyndeck(self, model, tmpl, name_suffix):
        # Create a dynamic deck. This also sets it as the current deck
        deckName = PREFIX + "-" + model['name'] + '-' + name_suffix
        dynDeckId = mw.col.decks.newDyn(deckName)
        dynDeck = mw.col.decks.get(dynDeckId)
        searchStr =  "note:'%s' card:'%s'" % (model['name'], tmpl['name'])
        dynDeck['delays'] = None
        dynDeck['terms'][0] =  [searchStr, 100, 0] #search, limit, current
        dynDeck['resched'] = True
        mw.col.decks.save(dynDeck)
        mw.col.sched.rebuildDyn(dynDeckId)
    
    def clean_up(self):
        print "Cleaning up SuperStyler junk..."
        
        mw.progress.start()
        decks_to_delete = []
        for deck in mw.col.decks.all():
            if deck['name'].startswith(PREFIX):
                decks_to_delete.append(deck)
        for deck in decks_to_delete:
            print "Deleting leftover deck: " + deck['name']
            mw.col.decks.rem(deck['id'])
        
        tmpls_to_delete = []
        for model in mw.col.models.all():
            for tmpl in model['tmpls']:
                if tmpl['name'].startswith(PREFIX):
                    tmpls_to_delete.append((model, tmpl))
    
        for (model, tmpl) in tmpls_to_delete:
            print "Deleting leftover tmpl: " + tmpl['name'] + " -- from model: " + model['name']
            mw.col.models.remTemplate(model, tmpl)
        
        print "Done!"
        mw.progress.finish()
    
    
# create menu items
ss = SuperStyler()
ss_menu = QAction("Super Styler", mw)
mw.connect(ss_menu, SIGNAL("triggered()"), ss.show_dialog)

# and add it to the tools menu
mw.form.menuTools.addAction(ss_menu)