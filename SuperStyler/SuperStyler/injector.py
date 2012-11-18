#from time import gmtime, strftime
#
#from aqt.utils import askUser
#from aqt.qt import *
#from aqt.webview import AnkiWebView
#from anki.hooks import addHook, wrap
#from aqt.clayout import CardLayout
#
#import utils
#import templateserver
#
#
#class Injector(object):
#    
#    def __init__(self):
#        self.inject()
#
#    def inject(self):
#       
#        css = model['css']
#        tmpl_q = tmpls['qfmt']
#        tmpl_a = tmpls['afmt']
#        
#        # Close any lingering servers
#        if _tmpl_server is not None:
#            templateserver.stop_server(_tmpl_server)
#        
#        # Start a new template server on a free port
#        port = utils.get_free_port()
#        _tmpl_server = templateserver.start_new_server("0.0.0.0", port)
#        
#        # Read our script into memory
#        scriptPath = os.path.join(os.path.dirname(__file__), 'script.js')
#        script = open(scriptPath, 'r').read()
#        
#        # Update the script with our machine's local network IP and port
#        url = str(utils.get_lan_ip()) + ':' + str(port)
#        script = script.replace('##AddressGoesHere##', url)
#        
#        # Create the template that we will inject javascript into
#        cardName = PREFIX + "-tmpl-" + strftime("%Y%m%d%H%M%S", gmtime())
#        new_tmpl = mw.col.models.newTemplate(cardName)
#        new_tmpl['qfmt'] = script + tmpl_q
#        new_tmpl['afmt'] = script + tmpl_a
#        
#        # Add it to the model we selected
#        mw.col.models.addTemplate(model, new_tmpl)
#        mw.col.models.save(model, True)
#                
#        # Create a dynamic deck. This also sets it as the current deck
#        deckName = PREFIX + "-deck-" + strftime("%Y%m%d%H%M%S", gmtime())
#        dynDeckId = mw.col.decks.newDyn(deckName)
#        dynDeck = mw.col.decks.get(dynDeckId)
#        searchStr = "card:'%s'" % (cardName)
#        dynDeck['delays'] = None
#        dynDeck['terms'][0] =  [searchStr, 100, 0] #search, limit, current
#        dynDeck['resched'] = True
#        mw.col.decks.save(dynDeck)
#        mw.col.sched.rebuildDyn(dynDeckId)
#        
#        # Redraw the card layout window to show the one we just created.
#        # Also, select it.
#        self.clayout.redraw()
#        self.clayout.selectCard(new_tmpl['ord'])
#        
#        _tmpl_server.set_CSS(css)
#        # Syncing can't be done with the CardLayout window open.
#        # We close it, do our sync, then open it up again.
#        self.clayout.reject()
#        mw.onSync()
#        
## TODO: I should probably put all this method wrapping inside the SuperStyler class
## ----------------------------------------------------------------------------------
#def mySetupButtons(self):
#    b = QPushButton("SuperStyler")
#    b.connect(b, SIGNAL("clicked()"), lambda: SuperStyler(self))
#    self.buttons.addWidget(b)
#
#def mySelectCard(self, idx):
#    # I'm going to disable editing the template for now. Only leave CSS
#    # editable. I'll need to figure out a good way to handle the template
#    # some other time.
#    if not hasattr(self, 'tab'):
#        return
#    
#    if self.tabs.tabText(idx).startswith(PREFIX):
#        self.tab['tform'].front.setReadOnly(True)
#        self.tab['tform'].back.setReadOnly(True)
#    else:
#        self.tab['tform'].front.setReadOnly(False)
#        self.tab['tform'].back.setReadOnly(False)
#
#def mySaveCard(self):
#    # Only do CSS for now.
#    if _tmpl_server is not None:
#        text = self.tab['tform'].css.toPlainText()
#        _tmpl_server.set_CSS(text)
#        
#        
## We keep only one server instance
#_tmpl_server = None
#
##def cleanUp():
##    print "Cleaning up SuperStyler junk..."
##    decks_to_delete = []
##    for deck in mw.col.decks.all():
##        if deck['name'].startswith(PREFIX):
##            decks_to_delete.append(deck)
##    for deck in decks_to_delete:
##        print "Deleting leftover deck: " + deck['name']
##        mw.col.decks.rem(deck['id'])
##    
##    tmpls_to_delete = []
##    for model in mw.col.models.all():
##        for tmpl in model['tmpls']:
##            if tmpl['name'].startswith(PREFIX):
##                tmpls_to_delete.append((model, tmpl))
##            
##    for (model, tmpl) in tmpls_to_delete:
##        print "Deleting leftover tmpl: " + tmpl['name'] + " -- from model: " + model['name']
##        mw.col.models.remTemplate(model, tmpl)
##        
##    mw.reset() #update UI
##
##
#
##
### On collection load, clean up junk we might have left over in the collection 
### in the event of improperly closing the application.
##addHook("profileLoaded", cleanUp)
##   
##
##
##def myReject(self):
##    pass
##    #cleanUp()
##
## 
##CardLayout.setupButtons = wrap(CardLayout.setupButtons, mySetupButtons)
##CardLayout.selectCard = wrap(CardLayout.selectCard, mySelectCard)
##CardLayout.saveCard = wrap(CardLayout.saveCard, mySaveCard)
##CardLayout.reject = wrap(CardLayout.reject, myReject)