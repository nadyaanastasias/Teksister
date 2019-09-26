import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import base64

key = "nadya:password"
encodedKey = "Basic " + str(base64.b64encode(key.encode("utf-8")),"utf-8")

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        print ("Send Header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print ("Test")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write(b'No Auth Header Received')
            pass
        elif self.headers.get('Authorization') == encodedKey:
            return SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            print(self.headers.get('Authorization'))
            self.wfile.write(b'Not Authenticated')
            pass

port = 8880
httpd = http.server.HTTPServer(('', port), RequestHandler)
print("Serving At Port", port)
httpd.socket = ssl.wrap_socket(httpd.socket,keyfile='C:/Users/Nadya/Desktop/Server/my-key.pem', certfile='C:/Users/Nadya/Desktop/Server/my-cert.pem', server_side=True)
httpd.serve_forever()