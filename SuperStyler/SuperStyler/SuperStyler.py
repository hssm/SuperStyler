from time import gmtime, strftime

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

import selector, utils
from templateserver import TemplateHandler, TemplateServer
import templateserver

PREFIX = '##SuperStyler'

def cleanUp():
    print "Cleaning up SuperStyler junk..."
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
        
    mw.reset() #update UI

def ssLaunch():
    SelectStyle(mw)


# create a new menu item
action = QAction("Super Styler", mw)
# set it to call ssLaunch when it's clicked
mw.connect(action, SIGNAL("triggered()"), ssLaunch)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

# On collection load, clean up junk we might have left over in the collection 
# in the event of improperly closing the application.
addHook("profileLoaded", cleanUp)

class SelectStyle(QDialog):

    def __init__(self, mw):
        # Form setup
        QDialog.__init__(self, mw)
        self.mw = mw
        self.form = selector.Ui_Dialog()
        self.form.setupUi(self)
        self.form.btnStart.setDisabled(True)

        # Add events for comboBox selection
        self.connect(self.form.comboModelSelect, SIGNAL('currentIndexChanged(QString)'), self.onModelSelect)
        self.connect(self.form.comboTmplSelect, SIGNAL('currentIndexChanged(QString)'), self.onTmplSelect)
        # Add event for Start button
        self.connect(self.form.btnStart, SIGNAL('clicked()'), self.onBtnStart)
                                
        # Make a combo box of all model names in the collection
        model_names = [model['name'] for model in mw.col.models.all()]
        self.form.comboModelSelect.addItems(model_names)

        # Select first item as a default
        self.form.comboModelSelect.setCurrentIndex(0)
        
        # Start UI (show it)
        self.exec_()


    def onModelSelect(self, model_name):
        print "On Model Select", model_name
        self.current_model = mw.col.models.byName(model_name)
        # Make a combo box of all templates (by name) in the chosen model
        tmpl_names = [tmpl['name'] for tmpl in self.current_model['tmpls']]
        self.form.comboTmplSelect.clear()
        self.form.comboTmplSelect.addItems(tmpl_names)

        # Select first item as a default
        self.form.comboTmplSelect.setCurrentIndex(0)
        
        # The first option will be selected by default, so enable the start button
        self.form.btnStart.setEnabled(True)
        

    def onTmplSelect(self, tmpl_name):
        print "On TMPL Select", tmpl_name
        tmpls = self.current_model['tmpls']
        for tmpl in tmpls:
            if tmpl['name'] == tmpl_name:
                self.current_tmpl = tmpl
                break

    # Start was clicked! We now need to do six things:
    # *1 - Grab the template and CSS data
    # 2 - Start a small web server to serve that data
    # *3 - Create a new template to mess around with
    # 4 - Inject our magic javascript into the new template with our web server's
    #     IP address
    # 5 - Create a cram deck with that new template.
    # 6 - Sync the deck so it's available everywhere
    
    def onBtnStart(self):      
        css = self.current_model['css']
        tmpl_q = self.current_tmpl['qfmt']
        tmpl_a = self.current_tmpl['afmt']
        
        # Read our script into memory
        scriptPath = os.path.join(os.path.dirname(__file__), 'script.js')
        script = open(scriptPath, 'r').read()
        # update the script with our machine's local network IP
        script = script.replace('##AddressGoesHere##', utils.get_lan_ip())
        
        # Create the template that we will inject javascript into
        cardName = PREFIX + "-tmpl-" + strftime("%Y%m%d%H%M%S", gmtime())
        new_tmpl = self.mw.col.models.newTemplate(cardName) #this also sets it as the current model
        new_tmpl['qfmt'] = script + tmpl_q
        new_tmpl['afmt'] = script + tmpl_a
        
        # Add it to the model we selected
        self.mw.col.models.addTemplate(self.current_model, new_tmpl)
        self.mw.col.models.save(self.current_model, True)

        # Create a dynamic deck. This also sets it as the current deck
        deckName = PREFIX + "-deck-" + strftime("%Y%m%d%H%M%S", gmtime())
        dynDeckId = self.mw.col.decks.newDyn(deckName)
        dynDeck = self.mw.col.decks.get(dynDeckId)
        searchStr = "card:'%s'" % (cardName)
        dynDeck['delays'] = None
        dynDeck['terms'][0] =  [searchStr, 100, 0] #search, limit, current
        dynDeck['resched'] = True
        self.mw.col.decks.save(dynDeck)
        self.mw.col.sched.rebuildDyn(dynDeckId)
        
        # TODO: find next open port instead of hardcoding this one
        ts = templateserver.start_new_server("0.0.0.0", 9998)
        ts.set_CSS(css)
        
        #self.mw.onSync()
        self.mw.reset() #update UI
        