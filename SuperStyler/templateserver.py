# Copyright (C) Houssam Salem <houssam.salem.au@gmail.com>
# License: GPLv3; http://www.gnu.org/licenses/gpl.txt
#
# Functions that modify the collection to make the plugin work. Includes
# cleanup routines for when we're done modifying things.
#
# A simple web server that hosts the changing stylesheet.
#
# This post helped lots:
# http://www.mlsite.net/blog/?p=80


import threading
import os
import re
from stdLocal import BaseHTTPServer, SocketServer

from aqt import mw

import utils
import deckfunctions as df

# Use the user-specified port 
use_manual_port = False
# User-specified port number
port = 0 


# Templates we are hosting, indexed by model id
hosted_tmpls = {}

server_started = False
        
class HostedTmpl:

    def __init__(self, model, tmpl, ss_tmpl):
        self.model = model
        self.tmpl = tmpl
        self.ss_tmpl = ss_tmpl
        
class TemplateHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def __init__(self, request, client_address, server):
        try:
            BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        except IOError: # We'll gladly ignore broken pipes.
            return

    def log_message(self, format, *args):
        """Turn off logging since Anki shows these as errors."""
        return

    def do_HEAD_CSS(self):
        self.send_response(200)
        self.send_header("Content-type", "text/css")
        self.send_header('Cache-control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()

    def do_HEAD_HTML(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Cache-control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()

    def do_HEAD_404(self):
        self.send_response(404)
        self.end_headers()        

    def do_HEAD_500(self):
        self.send_response(500)
        self.end_headers()

    def do_GET(self):
        
        m = re.search("/(.+)/(.+)", self.path)
        if m is None:
            return
        
        model_id = int(m.group(1))
        path = m.group(2)
        
        if model_id not in hosted_tmpls.keys():
            return
        
        if path.startswith("style.css"):
            self.do_HEAD_CSS()
            ht = hosted_tmpls[model_id]
            self.wfile.write(ht.model['css'])
        elif path == "question.html":
            # TODO?
            self.do_HEAD_HTML()
            self.wfile.write(hosted_tmpls[model_id].tmpl['qfmt'])
        elif path == "answer.html":
            # TODO?
            self.do_HEAD_HTML()
            self.wfile.write(hosted_tmpls[model_id].tmpl['afmt'])
        else:
            self.do_HEAD_404()
            self.wfile.write("Not found")

class TemplateServer(BaseHTTPServer.HTTPServer):
    
    def __init__(self, server_address, RequestHandlerClass):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)       
        self.RequestHandlerClass.question_template = None
        self.RequestHandlerClass.answer_template = None
        self.RequestHandlerClass.stylesheet = None
        
    def set_CSS(self, css_text):
        self.RequestHandlerClass.stylesheet = css_text
    
    def set_question(self, question):
        self.RequestHandlerClass.question_template = question
    
    def set_answer(self, answer):
        self.RequestHandlerClass.answer_template = answer



        
def add_template(model, tmpl):

    global server_started
    # Delay starting the server until we have at least one thing to host in it
    if not server_started:
        _start_server()
        server_started = True

    ss_tmpl = df.get_ss_tmpl(model)
    # In case the user deleted it while the SuperStyler window is open
    if ss_tmpl is None:
        return
    
    # Load the javascript we will inject into each template
    scriptPath = os.path.join(os.path.dirname(__file__), 'script.js')
    script = open(scriptPath, 'r').read()


    # Update the javascript with the full address to this template
    url = "%s:%s/%s" % (str(utils.get_lan_ip()), port, model['id']) 
    script = script.replace('##AddressGoesHere##', url)
    
    ss_tmpl['qfmt'] = script + tmpl['qfmt']
    ss_tmpl['afmt'] = script + tmpl['afmt']
    mw.col.models.save(model, True)
    
    ht = HostedTmpl(model, tmpl, ss_tmpl)
    hosted_tmpls[model['id']] = ht

def remove_template(model):
    if model['id'] in hosted_tmpls:
        del hosted_tmpls[model['id']]

def update_stylesheet(model, text):
    ht = hosted_tmpls[model['id']]
    ht.model['css'] = text

def update_qfmt(model, tmpl, qfmt):
    pass

def update_afmt(model, tmpl, afmt):
    pass

def is_hosted(model, tmpl):
    if model['id'] in hosted_tmpls.keys():
        hosted_name = hosted_tmpls[model['id']].tmpl['name']
        if hosted_name == tmpl['name']:
            return True
    return False

def _start_server():
    if use_manual_port:
        _port = port
    else:
        _port = utils.get_free_port()
        
    try:
        ip = "0.0.0.0"
        ts = TemplateServer((ip, _port), TemplateHandler)    
        t_name = "SuperStyler template server thread"
        t = threading.Thread(target=ts.serve_forever, name=t_name)
        t.daemon = True
        t.start()
    except SocketServer.socket.error, e:
        from aqt.utils import showInfo
        s = ("SuperStyler failed to open a server. Make sure the chosen port "
             "(%s) is not in use.\n\nError was: %s") % (_port, str(e))
        showInfo(s)
        

