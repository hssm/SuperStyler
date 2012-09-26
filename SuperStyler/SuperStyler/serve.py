import BaseHTTPServer

class UpdatingTemplateHandler(BaseHTTPServer.BaseHTTPRequestHandler):
     
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if self.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            self.wfile.write(self.getCssText())
            print "Sending a stylesheet..."
        elif self.path == "/question":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()            
            self.wfile.write("Here is my question:")
        elif self.path == "/answer":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Here is my answer:")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("404 - Not found")

    def getCssText(self):
        if self.useFile:
            #open the file here and return its contents
            return ""
        else:
            #return text from some source
            return UpdatingTemplateHandler.cssText
 
    # this'll do for now   
    cssText = """
.card
{
  position: fixed;
  background-color: #533;
  height: 100%;
  margin: 0;
  padding: 0;
}
"""

if __name__ == '__main__':
    print "Starting server on port 9999...",
    httpd = BaseHTTPServer.HTTPServer(("0.0.0.0", 9999), UpdatingTemplateHandler)
    print "Started."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
