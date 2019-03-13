# CIS 457 Project 1: Multi-Threading FTP Server

These programs are multi-threaded FTP client/server programs primarily designed for Mac OS using pyftpdlib and python 3.7. Pyftpdlib is not needed to run the program if it is run on Mac OS, as the module is bundled together into an executable via pyinstaller. Python 3 is required however. If you do not have it, you can download it at https://www.python.org/downloads/.

The server program binds to a port and listens for requests from a client. After a client connects to the server, the server waits for commands. When the client sends a terminate message (quit), the server terminates the connection and waits for the next connection.

## How to Run:

This program requires that you first start the server ("ftp_server") before the client ("ftp_client") will be able to connect. Download all of the files from this Github to ensure you have all of the necessary dependencies.

### Server:

#### Mac:

To start the server, run the executable mt_ftp_server/Server/dist/ftp_server by double clicking on the file. This will open a window in the terminal prompting to enter the ip/hostname of your computer in order to host the server. Once the server has been started, it will wait and listen for any requests by clients. By default, the server's directory is the user's home directory. 

#### Linux:

If you would like to run the server on Linux or Windows, the module pyftpdlib must be installed. This can be installed easily via the Terminal/PowerShell command 'pip install pyftpdlib' (or pip3 if your system's default python version is Python 2). This guide can assist with installing pip if you do not already have it: https://www.makeuseof.com/tag/install-pip-for-python/. When pyftpdlib has been installed, you can run 'ftp_server.py' via the command 'python path/to/repository/mtp_ftp_server/Server/ftp_server.py'(or python3 if your system's default python version is Python 2).  Once the server has been started, it will wait and listen for any requests by clients. The server's directory is the directory where this file was executed (in this case the 'Server' folder). 
  
### Client:

To start, open another window in Terminal/PowerShell and run the command "python3 (or python if python 3 is natively installed) path/to/repository/mt_ftp_server/Client/ftp_client.py". By default, the clients's directory is the directory in which the program was executed (in this case the 'Client' folder). The usage for the client is as follows:

1.	CONNECT <server name/IP address> <server port>: This command allows a client to connect to a server. The arguments are the IP address of the server and the port number on which the server is listening for connections. For you, this will be the ip/hostname inputted on the server and the port number 1026, which is the port number set on the server. This command must be made before any other commands can be made.

2.	LIST: When this command is sent to the server, the server returns a list of the files in the current directory on which it is executing. The client will get the list and display it on the screen.

3.	RETRIEVE <filename>: This command allows a client to get a file specified by its filename from the server. This will bring the file from the server directory over to the client directly, and will overwrite any files with the same name.

4.	STORE <filename>: This command allows a client to send a file specified by its filename to the server. This will bring the file from the client directory over to the server directly, and will overwrite any files with the same name.

5.	QUIT: This command allows a client to terminate the control connection. When the ftp_server receives the quit command it will close its end of the connection.The server will remain online, however.
