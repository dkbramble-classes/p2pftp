from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from socketserver import ThreadingMixIn
#import SocketServer
# https://blog.anvileight.com/posts/simple-python-http-server/
# https://gist.github.com/bradmontgomery/2219997
# curl -d "username_hostname_connection" http://localhost

userInfo = {}
userFiles = {}
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
        # If the information is about a user, store the username with the hostname and connection as a smaller dictionary
        if parsedBody[0] == "User":
            userInfo[parsedBody[1]] = {
                "hostname": parsedBody[2],
                "connection": parsedBody[3]
            }
        #Otherwise if the information is for a file, store the file name and descritpion as a list of dictionaries under the username
        elif parsedBody[0] == "File":
            userFiles[parsedBody[1]].add({
                "fileName": parsedBody[2],
                "fileDescriptor": parsedBody[3]
            } )
        else:
            print("Didn't receive proper request")
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