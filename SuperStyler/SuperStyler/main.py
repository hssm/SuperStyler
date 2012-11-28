import time
import re

from aqt import mw
from aqt.qt import *


import utils
import templateserver
import maindialog
import editor

# Note: ss = SuperStyler

PREFIX = '##Styler'

servers = {}
has_instance = False    # Keep only 1 instance of the plugin window

class SuperStyler(object):
        
    def show_dialog(self):
        global has_instance
        
        if has_instance:
            return
        has_instance = True
        
        d = QDialog(mw)
        self.diag = d
        self.frm = maindialog.Ui_Dialog()
        self.frm.setupUi(d)
        self.frm.webView.page().setLinkDelegationPolicy(
                QWebPage.DelegateAllLinks)       
        self.frm.webView.setHtml(self.get_body())
        self.frm.webView.setStyleSheet(self.get_stylesheet())
        mw.connect(self.frm.webView, SIGNAL("linkClicked(QUrl)"),
                   self.link_clicked)
        mw.connect(d, SIGNAL("rejected()"), self.on_close)
        d.show()
    
    def get_body(self):
        global servers
        
        if self.need_prepare():
            return self.get_prepare_body()
        else:
            body =\
"""
<table width=100%%>
<tr>
<th align=left>Note</th>
<th align=left>Card</th>
<th align=left>Deck/Server</th>
<th align=left>Editor</th>
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
        """Get the HTML that comprises the row for a model in the main table."""
        
        tmpl = self.get_ss_tmpl(model)
        cards = mw.col.findCards("note:'%s' card:'%s'" % (model['name'], tmpl['name']))
        nonempty_tmpl = self.get_nonempty_ss_tmpl(model) is not None       
        has_cards = len(cards) > 0
        has_dyndeck = self.get_ss_dyndeck(model) is not None 
        
        # Cards are deleted when the template is blanked. But if, for some 
        # reason, we have already blanked the template but the cards still 
        # exist, we need to make available the clear option.
        if nonempty_tmpl or has_cards or has_dyndeck:
            m_column = ("""%s <a style='color: #c44;' href="clear note:'%s' tmpl:'%s'">[clear]</a>""" % 
                (model['name'], model['id'], tmpl['ord'])) 
        else:
            m_column = model['name']
        
        row =\
"""
<tr style="background-color:%s;">
<td>%s</td>
<td/>
<td/>
<td/>
""" % (color, m_column)
        return row
    
    def get_tmpl_row(self, model, tmpl, color):

        deck_column = ("""<td><a href="create note:'%s' tmpl:'%s'">Create</a></td>""" %
                           (model['id'], tmpl['ord'])) 

        global servers
        has_server = False
        if (model['name'] in servers and
            servers[model['name']].id == tmpl['name']):
            has_server = True
            
        editor_column = "<td/>"
        if has_server and self.get_ss_dyndeck(model) is not None:
            editor_column = ("""<td><a style='color: #272' href="open note:'%s' tmpl:'%s'">[Open]</a></td>""" %
                             (model['id'], tmpl['ord']))       
        row =\
"""
<tr style="background-color:%s;">
<td/>
<td>%s</td>
%s
%s
""" % (color, tmpl['name'], deck_column, editor_column)
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
        elif link.startswith("clear"):
            self.handle_clear(link)
        elif link.startswith("create"):
            self.handle_create(link)
        elif link.startswith("open"):
            self.handle_open(link)
        else:
            pass
        
        # Redraw SuperStyler window
        self.frm.webView.setHtml(self.get_body())
        
        mw.reset() #update anki UI
        mw.progress.finish()

    def handle_clear(self, link):
        m = re.search("clear note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
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
        
        dyndeck = self.get_ss_dyndeck(model)
        if dyndeck is not None:
            mw.col.decks.rem(dyndeck['id'])
    
    def handle_create(self, link):
        m = re.search("create note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        self.start_template_server(model, tmpl)
        print "MODEL: %s   ---  TMPL: %s  " % (model['name'], tmpl['name'])
            
    def handle_open(self, link):
        m = re.search("open note:'(.+)' tmpl:'(.+)'", link)
        model_id = m.group(1)
        tmpl_ord = int(m.group(2))
        model = mw.col.models.get(model_id)
        tmpl = model['tmpls'][tmpl_ord]
        server = self.get_open_server(model, tmpl)
        
        d = QDialog(mw)
        ed = editor.Dialog()
        ed.setupUi(mw, model, server, d)
        d.connect(d, SIGNAL("rejected()"), lambda: self.diag.setVisible(True))

        self.diag.setVisible(False)
        d.show()

    
    def need_prepare(self):
        """Check if the plugin needs to create a SuperStyler card type
        for any of the models. If any are missing it, return True."""
        
        for model in mw.col.models.all():
            if self.get_ss_tmpl(model) is None:
                return True
        return False
    
    def get_ss_tmpl(self, model):
        """SuperStyler template if the model has one, or None if not."""
        for tmpl in model['tmpls']:
            if tmpl['name'].startswith(PREFIX):
                return tmpl
        return None

    def get_ss_dyndeck(self, model):
        """SuperStyler dyndeck if one exists for the model, or None if not."""
        for deck in mw.col.decks.all():
            m = re.match(PREFIX+"-(.+)-"+PREFIX, deck['name'])
            if m is not None:
                deck_name = m.group(1) 
                if model['name'] == deck_name:
                    return deck
        return None
    
    def get_nonempty_ss_tmpl(self, model):
        """Returns the SuperStyler template if it's non-empty, else None."""
        tmpl = self.get_ss_tmpl(model)
        if tmpl['qfmt'] or tmpl['afmt']:
            return tmpl
        return None

    def get_open_server(self, model, tmpl):
        """Returns a TemplateServer for the model's template if one exists,
        or None if not."""
       
        if model['name'] in servers:
            server = servers[model['name']]
            if server is not None and server.id == tmpl['name']:
                return server
        return None
    
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
        server = templateserver.start_new_server("0.0.0.0", port, tmpl['name'])
        
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
        
        # Add it to our global list of running servers. Close and remove any
        # that are already running and belong to the same model (since we have
        # one stylesheet per model, we should only have one editor as well).
        global servers
        if model['name'] in servers:
            old_srv = servers[model['name']]
            templateserver.stop_server(old_srv) 
            
        servers[model['name']] = server
        server.set_CSS(model['css'])
        
        self.create_styler_dyndeck(model, srv_tmpl)
        
    
    def create_styler_dyndeck(self, model, tmpl):
        # Create a dynamic deck. This also sets it as the current deck
        deckName = PREFIX + "-" + model['name'] + '-' + tmpl['name']
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
            print "Deleting ss deck: " + deck['name']
            mw.col.decks.rem(deck['id'])
        
        tmpls_to_delete = []
        for model in mw.col.models.all():
            for tmpl in model['tmpls']:
                if tmpl['name'].startswith(PREFIX):
                    tmpls_to_delete.append((model, tmpl))
    
        for (model, tmpl) in tmpls_to_delete:
            print "Deleting ss tmpl: " + tmpl['name'] + " -- from model: " + model['name']
            mw.col.models.remTemplate(model, tmpl)
        
        print "Done!"
        mw.progress.finish()
    
    def on_close(self):
        global has_instance
        has_instance = False
        
# create menu items
ss = SuperStyler()
ss_menu = QAction("Super Styler", mw)
mw.connect(ss_menu, SIGNAL("triggered()"), ss.show_dialog)

# and add it to the tools menu
mw.form.menuTools.addAction(ss_menu)