# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# Functions that modify the collection to make the plugin work. Includes
# cleanup routines for when we're done modifying things.

import re

from aqt import mw

PREFIX = '##Styler'

def need_prepare():
    """Check if the plugin needs to create a SuperStyler card type
    for any of the models. If any are missing it, return True."""
    
    for model in mw.col.models.all():
        if get_ss_tmpl(model) is None:
            return True
    return False

def check_full_cleanup():
    """Check if there is anything in the collection that was created
    by this plugin. Return True if anything is found."""
    
    for deck in mw.col.decks.all():
        if deck['name'].startswith(PREFIX):
            return True
    
    for model in mw.col.models.all():
        for tmpl in model['tmpls']:
            if tmpl['name'].startswith(PREFIX):
                return True

def need_model_clear(model):
    """Check if there is anything relating to a model that lingers in
    the collection that can be cleaned up."""
    
    # The plugin creates templates, cards, and dyndecks. If cards or 
    # dyndecks exist for this model, or if the SuperStyler template
    # is non-empty (since it generates cards), we signal the need for
    # a clear.

    tmpl = get_ss_tmpl(model)
    cards = mw.col.findCards("note:'%s' card:'%s'" % (model['id'], tmpl['name']))
    nonempty_tmpl = get_nonempty_ss_tmpl(model) is not None       
    has_cards = len(cards) > 0
    has_dyndeck = get_ss_dyndeck(model) is not None
    
    if nonempty_tmpl or has_cards or has_dyndeck:
        return True
    else:
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
        m = re.match(PREFIX+"-(.+?)-(.+)", deck['name'])
        if m is not None:
            model_id = m.group(1)
            model_name = m.group(2)
            if model_id == str(model['id']):
                return deck
    return None
    
def get_nonempty_ss_tmpl(model):
    """Returns the SuperStyler template if it's non-empty, else None."""
    
    tmpl = get_ss_tmpl(model)
    if tmpl['qfmt'] or tmpl['afmt']:
        return tmpl
    return None

def prepare_collection():
    """Create an empty template for every model."""
    
    mw.progress.start()
    for model in mw.col.models.all():
        if not (get_ss_tmpl(model)):
            tmpl_name = PREFIX + "-" + str(model['id'])
            new_tmpl = mw.col.models.newTemplate(tmpl_name)
            new_tmpl['qfmt'] = ''
            new_tmpl['afmt'] = ''
            mw.col.models.addTemplate(model, new_tmpl)
            mw.col.models.save(model, True)

    mw.progress.finish()

def create_styler_dyndeck(model):
    """Create a dynamic deck. This also sets it as the current deck. The
    name is decided based on the model, and an internal prefix."""
    
    ss_tmpl = get_ss_tmpl(model)
    deckName = PREFIX + "-" + str(model['id']) + "-" + model['name']
    dynDeckId = mw.col.decks.newDyn(deckName)
    dynDeck = mw.col.decks.get(dynDeckId)
    searchStr =  "note:'%s' card:'%s'" % (model['name'], ss_tmpl['name'])
    dynDeck['delays'] = None
    dynDeck['terms'][0] =  [searchStr, 25, 0] #search, limit, current
    dynDeck['resched'] = True
    mw.col.decks.save(dynDeck)
    mw.col.sched.rebuildDyn(dynDeckId)

def empty_tmpl_and_cards(model, tmpl):
    """Set the template content to blank and delete any cards that were
    originally generated by this template."""
    
    # Empty the template
    tmpl['qfmt'] = ''
    tmpl['afmt'] = ''
    mw.col.models.save(model, True)
    
    # Copied this from models.py -> remTemplate().
    cids = mw.col.db.list("""
    select c.id from cards c, notes f where c.nid=f.id and mid = ? and ord = ?""",
                                 model['id'], tmpl['ord'])
    mw.col.remCards(cids, notes=False)
    
def clean_up():
    """Remove any templates (and thus cards) and dynamic decks created by
    this plugin. Effectively, this will remove any trace of the plugin from
    the collection."""
    
    mw.progress.start()
    decks_to_delete = []
    for deck in mw.col.decks.all():
        if deck['name'].startswith(PREFIX):
            decks_to_delete.append(deck)
    
    for deck in decks_to_delete:
        mw.col.decks.rem(deck['id'])
    
    tmpls_to_delete = []
    for model in mw.col.models.all():
        for tmpl in model['tmpls']:
            if tmpl['name'].startswith(PREFIX):
                tmpls_to_delete.append((model, tmpl))

    for (model, tmpl) in tmpls_to_delete:
        mw.col.models.remTemplate(model, tmpl)
    
    mw.progress.finish()