# This post helped lots:
# http://www.mlsite.net/blog/?p=80

import BaseHTTPServer

class TemplateHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.question_template = None
        self.answer_template = None
        self.stylesheet = None
        
    def do_HEAD_CSS(self):
        self.send_response(200)
        self.send_header("Content-type", "text/css")
        self.end_headers()

    def do_HEAD_HTML(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_HEAD_404(self):
        self.send_response(404)
        self.end_headers()        

    def do_HEAD_500(self):
        self.send_response(500)
        self.end_headers()

    def do_GET(self):
        if self.path == "/style.css":
            if self.stylesheet is None:
                self.do_HEAD_500()
                self.wfile.write("Stylesheet has not been set")
            else:
                self.do_HEAD_CSS()
                self.wfile.write(self.stylesheet)
        elif self.path == "/question.html":
            if self.question_template is None:
                self.do_HEAD_500()
                self.wfile.write("Question template has not been set")
            else:
                self.do_HEAD_HTML()
                self.wfile.write(self.question_template)
        elif self.path == "/answer.html":
            if self.answer_template is None:
                self.do_HEAD_500()
                self.wfile.write("Answer template has not been set")
            else:
                self.do_HEAD_HTML()
                self.wfile.write(self.answer_template)
        else:
            self.do_HEAD_404()
            self.wfile.write("Not found")

class TemplateServer(BaseHTTPServer.HTTPServer):
    
    def __init__(self, server_address, RequestHandlerClass):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)

    def set_CSS(self, css_text):
        self.RequestHandlerClass.stylesheet = css_text
    
    def set_question(self, question):
        self.RequestHandlerClass.question_template = question
    
    def set_answer(self, answer):
        self.RequestHandlerClass.answer_template = answer

if __name__ == '__main__':
    
    print "Starting server on port 9999...",
    ts = TemplateServer(("0.0.0.0", 9999), TemplateHandler)
    print "Started."
    
    # Add some dummy data just to test it
    css = \
"""
.card
{
  position: fixed;
  background-color: #533;
  height: 100%;
  margin: 0;
  padding: 0;
}
"""   
    ts.set_question("This is a question!")
    ts.set_answer("This is an answer!")
    ts.set_CSS(css)
    
    try:
        ts.serve_forever()
    except KeyboardInterrupt:
        pass
    ts.server_close()
