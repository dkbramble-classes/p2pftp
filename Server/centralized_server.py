from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
#import SocketServer
# https://blog.anvileight.com/posts/simple-python-http-server/
# https://gist.github.com/bradmontgomery/2219997
# curl -d "username_hostname_connection" http://localhost

#users
class Database(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        strBody = str(body, 'utf-8')
        parsedBody = strBody.split("_")
        print("This is the body: " + strBody)
        self.send_response(200)
        self.end_headers()

        #This is all for response to request caller
        # response = BytesIO()
        # response.write(b'This is POST request. ')
        # response.write(b'Received: ')
        # response.write(body)
        # self.wfile.write(response.getvalue())
        
def run(server_class=HTTPServer, handler_class=Database, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    run()