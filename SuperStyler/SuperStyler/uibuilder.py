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
<a href="clean">Clean up</a>
"""
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
    cards = mw.col.findCards("note:'%s' card:'%s'" % (model['name'], tmpl['name']))
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

    deck_column = ("""<td><a href="create note:'%s' tmpl:'%s'">Initialize</a></td>""" %
                       (model['id'], tmpl['ord'])) 

    has_server = False
    if (model['name'] in df.servers and
        df.servers[model['name']].id == tmpl['name']):
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
<p>Explain what happens here!</p>
<a href="clean">Clean up</a>
""" 
    
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