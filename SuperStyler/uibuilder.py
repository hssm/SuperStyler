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
"""
        s = ''
        color1 = '#ccc'
        color2 = '#eee'
        
        warn_clear_first = False
        
        for model in mw.col.models.all():
            need_clear = df.need_model_clear(model)
            if need_clear:
                warn_clear_first = True                
            s += get_model_row(model, color1, need_clear=need_clear)
            for tmpl in model['tmpls']:
                if tmpl['name'].startswith(df.PREFIX):
                    continue
                s += get_tmpl_row(model, tmpl, color1)
            (color1, color2) = (color2, color1)
        
        if warn_clear_first:
            body = body + _get_clear_warning() 
        
        body = body + _get_cleanup_portion()
        return body % s
                    
    
def get_model_row(model, color, need_clear):
    """Get the HTML that comprises the row for a model in the main table."""

    tmpl = df.get_ss_tmpl(model)
    if need_clear:
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
<b>Preparing the collection will create a card type in all of your models</b>
so you only have to do a full sync once. These cards will appear in the card
editor as "##Styler-xxx". Their templates will be populated and cleared during
use of the plugin; do not modify them yourself.
</p>
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

def _get_clear_warning():
    return\
"""
<div style="padding: 1em 0">
<b style="background-color: #fcc;">Warning!</b> You have SuperStyler cards in your collection. Be sure not to review
cards normally until you have removed them by clicking the <span style="color: #c44;">[clear]</span> link above.
</div>
"""

    

def _get_cleanup_portion():
    if not df.check_full_cleanup():
        return ""
    else:
        return\
"""
<div style="background-color: #f4eeee; padding: 1em 0;">
<b>Clean up collection</b>
<br>
<p>Clicking this link will remove all traces of SuperStyler from your collection.
A full sync will be triggered.</p>
<a href="clean">Clean up</a>
</div> 
"""
