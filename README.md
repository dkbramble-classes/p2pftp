# CIS 457 Project 2: GV-NAP File Sharing System
This is a file sharing system that allows users to access a distributed data storage system based on simple keyword search. These programs include a multi-threaded FTP GUI client/server host program and a multi-threaded HTTP centralized server which are primarily designed for Mac OS using pyftpdlib, requests, and python 3.7. The pyftpdlib and requests modules are not needed to run the program if it is ran on Mac OS, as the module is bundled together into an executable via pyinstaller. Python 3 is required however. If you do not have it, you can download it at https://www.python.org/downloads/. Both modules will have to be installed via pip in order to run on other systems.

-	The first part is the host system, which can query the server for files using keywords.  The host also has a file transfer client and server.  The ftp client allows a user to access files stored at the remote user locations.  The ftp server is responsible for providing file transfer services requested by a remote client.

-	The second part of the system is the centralized server, which provides a search facility that can be used to perform simple keyword searches.  The result of the search is the location of the remote resource.

## How to Run:
First, download all of the files from this Github to ensure you have all of the necessary dependencies. Preferably, this processes is done on at least two devices: One device for the centralized server and the host, and another device to run the other host program.

### Centralized Server (centralized_server.py):
To start, open a window in Terminal/PowerShell and run the command "python3 (or python if python 3 is natively installed) path/to/repository/p2pftp/Server/centralized_server.py".

### Host System (FTP Client/Server):

##:Mac OS
To start the host system, I dunno.
The host's ftp directory is the directory in which the program was executed (in this case the 'Host' folder).

##Linux

## Host Usage:

###:Connect to the Centralize Server (Top Section)
To get the most out of this program, you will want to first connect to the Centralized Server. To do this, fill in all of the input fields in the top section, choose your connection type, and then hit connect. You may also want to broadcast to others that you have files. To do this, edit the file_descriptions.txt file located in the same directory as the gui, and follow the same formatting as the provided files. This file will be uploaded ti the server when you hit connect. Other hosts will then be able to perform keyword searches based on the file descriptions that you provide.

###:Keyword Searches (Middle Section):
Once you have connected to the Centralized Server, you may perform a keyword search to see if any other hosts on your network have a file with a description that includes the given keyword. To search, enter any one word into the text box (more than one word is not accepted) MAYBE. The centralized server will then return all files where the keyword is present in the description and will place them in the table in the middle section of the GUI.

###:FTP Server/Client (Bottom Section):
Once you have seen the available hosts on the network you may wish transfer files to and from their machine. To do this, enter a command into the "Enter Command" text box and hit the "Go" button. The usage for the commands is as follows:

    CONNECT <server name/IP address> : This command allows the host to connect to another host's server. The arguments are the IP address of the server and the port number on which the server is listening for connections. For you, this will be the ip/hostname inputted (which will be displayed in the keyword search) on the server and the port number 1026, which is the port number set to every server. This command must be made before any other commands can be made.

    LIST: When this command is sent to the server, the server returns a list of the files in the current directory on which it is executing. The client will get the list and display it on the screen.

    RETRIEVE <filename>: This command allows a host to get a file specified by its filename from the server. This will bring the file from the server's directory over to the host's directory, and will overwrite any files with the same name.

    STORE <filename> : This command allows a host to get a file specified by its filename from the server. This will bring the file from the host's directory over to the server's directory, and will overwrite any files with the same name.

    QUIT: This command allows a client to terminate the control connection. When the other host receives the quit command it will close its end of the connection. No other new connections can be made until this command has been executed.
