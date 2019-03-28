from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from socketserver import ThreadingMixIn
import json
from urllib.parse import urlparse
import threading
# https://blog.anvileight.com/posts/simple-python-http-server/
# https://gist.github.com/bradmontgomery/2219997
# curl -d "username_hostname_connection" http://localhost

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

userInfo = {}
userFiles = {}
class Database(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #this is the function for the search command. Dane will use requests.get(url = URL, params = PARAMS) to request information
        query = urlparse(self.path).query
        print(query)
        searchStr = str(query)
        search = searchStr.split("=")
        x = 0
        response = {}
        print(search[1])
        for username in userFiles:
            for file in userFiles[username]:
                if search[1].lower() in userFiles[username][file].lower():
                    response[x] = {
                        "hostname": userInfo[username]["hostname"],
                        "connection": userInfo[username]["connection"],
                        "file": file,
                        "description": userFiles[username][file]
                    }
                    x += 1
                    print("File: " + file + " with Description: \"" + userFiles[username][file] + "\" found for search result.")

        self.send_response(200)
        self.end_headers()
        responseStr = json.dumps(response)
        print("The response should be: " + responseStr)
        self.wfile.write(responseStr.encode("utf-8"))
        # testResponse = "SEARCHED"
        # self.wfile.write(testResponse.encode("utf-8"))

        #query_components = dict(qc.split("=") for qc in query.split("&"))

        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        strBody = str(body, 'utf-8')
        parsedBody = strBody.split("_")
        # If the information is about a user, store the username with the hostname and connection as a smaller dictionary
        # This worked: curl -d "User_username2_hostname_connection" http://Lukes-MacBook-Pro-2.local
        if parsedBody[0] == "User":
            userInfo[parsedBody[1]] = {
                "hostname": parsedBody[2],
                "connection": parsedBody[3]
            }
            self.send_response(200)
            self.end_headers()
            response = "CONNECTED"
            self.wfile.write(response.encode("utf-8"))
            print("User " + parsedBody[1] + " connected to the server.")
        #Otherwise if the information is for a file, store the file name and descritpion as a list of dictionaries under the username
        #The JSON text that we send here to the server needs to have escape characters 
        # This worked: curl -d "File_Dane_{\"local_server.py\":\"Insert Description Here\",\"ftp_client.py\":\"Look, More Descriptions\",\"client_gui.py\":\"DESCRIPTIONS\" }" http://Lukes-MacBook-Pro-2.local
        elif parsedBody[0] == "File":
            jsonString = parsedBody[2]
            for x in range(3, len(parsedBody)):
                jsonString += "_" + str(parsedBody[x])
            print("jsonString: " + jsonString)
            datastore = json.loads(jsonString)
            if parsedBody[1] not in userFiles:
                userFiles[parsedBody[1]] = {}
            print("Files being uploaded:")
            for file in datastore:
                print(file)
                userFiles[parsedBody[1]][file] =  datastore[file]
            self.send_response(200)
            self.end_headers()
            response = "STORED"
            self.wfile.write(response.encode("utf-8"))
        #Return information as JSON payload 
        elif parsedBody[0] == "Quit":
            userInfo.pop(parsedBody[1])
            userFiles.pop(parsedBody[1])
            self.send_response(200)
            self.end_headers()
            response = "DELETED"
            self.wfile.write(response.encode("utf-8"))
            print("Disconnected user " + parsedBody[1])
        else:
            print("Didn't receive proper request. Request given: ", parsedBody)
        print("This is the body: " + strBody)
        #print("This is a file check: " + userFiles["Dane"]["local_server.py"] )

        #This is all for response to request caller
        # response = BytesIO()
        # response.write(b'This is POST request. ')
        # response.write(b'Received: ')
        # response.write(body)
        # self.wfile.write(response.getvalue())
        
def run(server_class=HTTPServer, handler_class=Database, port=80):
    server_address = '0.0.0.0'
    httpd = ThreadingSimpleServer((server_address, port), handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    run()
