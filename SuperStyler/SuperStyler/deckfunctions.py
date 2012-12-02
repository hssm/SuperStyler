import re
import time
import os

from aqt import mw

import utils
import templateserver

PREFIX = '##Styler'
servers = {}

def need_prepare():
    """Check if the plugin needs to create a SuperStyler card type
    for any of the models. If any are missing it, return True."""
    
    for model in mw.col.models.all():
        if get_ss_tmpl(model) is None:
            return True
    return False
    
def get_ss_tmpl(model):
    """SuperStyler template if the model has one, or None if not."""
    for tmpl in model['tmpls']:
        if tmpl['name'].startswith(PREFIX):
            return tmpl
    return None

def get_ss_dyndeck(model):
    """SuperStyler dyndeck if one exists for the model, or None if not."""
    for deck in mw.col.decks.all():
        m = re.match(PREFIX+"-(.+)-"+PREFIX, deck['name'])
        if m is not None:
            deck_name = m.group(1) 
            if model['name'] == deck_name:
                return deck
    return None
    
def get_nonempty_ss_tmpl(model):
    """Returns the SuperStyler template if it's non-empty, else None."""
    tmpl = get_ss_tmpl(model)
    if tmpl['qfmt'] or tmpl['afmt']:
        return tmpl
    return None

def get_open_server(model, tmpl):
    """Returns a TemplateServer for the model's template if one exists,
    or None if not."""
   
    if model['name'] in servers:
        server = servers[model['name']]
        if server is not None and server.id == tmpl['name']:
            return server
    return None
    
def prepare_collection():
    print "Preparing collection...",
    mw.progress.start()
    for model in mw.col.models.all():
        if not (get_ss_tmpl(model)):
            tmpl_name = PREFIX + "-" + str(int(time.time()*1000))
            new_tmpl = mw.col.models.newTemplate(tmpl_name)
            new_tmpl['qfmt'] = ''
            new_tmpl['afmt'] = ''
            mw.col.models.addTemplate(model, new_tmpl)
            mw.col.models.save(model, True)
    print "Done!"
    mw.progress.finish()
        
    
def start_template_server(model, tmpl):
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
    if model['name'] in servers:
        old_srv = servers[model['name']]
        templateserver.stop_server(old_srv) 
        
    servers[model['name']] = server
    server.set_CSS(model['css'])
    
    create_styler_dyndeck(model, srv_tmpl)
        
    
def create_styler_dyndeck(model, tmpl):
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
    
def clean_up():
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