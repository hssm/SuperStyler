# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# Get HTML markup to build the UI.
#
# I can't get CSS to work in the WebView, so I'm inlining style properties. Ugh. 

from aqt import mw

import deckfunctions as df

def get_body():
    
    if df.need_prepare():
        return get_prepare_body()
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
<br>
""" +  _get_cleanup_portion()
        s = ''
        color1 = '#ccc'
        color2 = '#eee'
        
        for model in mw.col.models.all():
            s += get_model_row(model, color1)
            for tmpl in model['tmpls']:
                if tmpl['name'].startswith(df.PREFIX):
                    continue
                s += get_tmpl_row(model, tmpl, color1)
            (color1, color2) = (color2, color1)
        return body % s
                    
    
def get_model_row(model, color):
    """Get the HTML that comprises the row for a model in the main table."""
    
    tmpl = df.get_ss_tmpl(model)
    cards = mw.col.findCards("note:'%s' card:'%s'" % (model['id'], tmpl['name']))
    nonempty_tmpl = df.get_nonempty_ss_tmpl(model) is not None       
    has_cards = len(cards) > 0
    has_dyndeck = df.get_ss_dyndeck(model) is not None 
    
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
    
def get_tmpl_row(model, tmpl, color):

    deck_column = ("""<td><a href="create note:'%s' tmpl:'%s'">Start</a></td>""" %
                       (model['id'], tmpl['ord'])) 

    has_server = False
    if (model['id'] in df.servers and
        df.servers[model['id']].id == tmpl['name']):
        has_server = True
        
    editor_column = "<td/>"
    if has_server and df.get_ss_dyndeck(model) is not None:
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
    
def get_prepare_body():
    return\
"""
<h1>Need to prepare collection</h1>
<br>
<a href="setup">Click here!</a>
<br>
<br>
<p>
<b>Details:</b>
<br>
To preserve the integrity of your collection, SuperStyler creates a new
card type for itself to modify. However, Anki requires a full sync every
time a new card type is created. This plugin is all about convenience, and a
full sync every session would be very inconvenient! 
<b>Preparing the collection will create a card type in all of your models</b>
so you only have to do a full sync once. These cards will appear in the card
editor starting with the name "##Styler". Their templates will be empty, so no
cards will be generated until you start a styling session. As long as they are
empty, there is no harm in keeping these templates. You will be cautioned
to clear any non-empty templates when you are done styling.</p>
<br>
<br>
""" + _get_cleanup_portion()
    
def get_stylesheet():
    """ I don't think this works :( """
    return\
"""
<style>
table
{
  background-color: #437;
  color: #fcc;
}
</style>
"""

def _get_cleanup_portion():
    if not df.need_cleanup():
        return ""
    else:
        return\
"""
<div style="background-color: #f4eeee;">
<b>Clean up collection</b>
<br>
<p>Clicking this link will remove all traces of SuperStyler from your collection.
A full sync will be triggered.</p>
<a href="clean">Clean up</a>
</div> 
"""
