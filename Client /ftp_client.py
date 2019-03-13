#This is a client program to connect with a multithreaded server using pyftpdlib. See requirements.txt for usage
#Authors: Luke Bassett, Dane Bramble, Patrik Kozak, Brendan Warnick
#Project for CIS 457
#Last Edited: February 9, 2019
import sys
import os
import socket
from ftplib import FTP

ftp = FTP('')

#error message that prints out the usage of the client
def usage_error(cmd):
    if cmd != '':
        print("improper usage of '" + cmd + "\'")
    print("Commands: \n\t CONNECT <server name/IP address> <server port> \n\t LIST \n\t RETRIEVE <filename> \n\t STORE <filename> \n\t QUIT")

#Connects to the host server
#host - hostname / IP address of the server
#port - the port number (1026)
def CONNECT(host, port):
    ftp.connect(host, int(port))
    ftp.login()
    ftp.cwd('.') #replace with your directory
    ftp.retrlines('LIST')
    print("connected to " + host)

#retrieves a list of files from the server directory
def LIST():
    ftp.retrlines('LIST')

#stores files to the server directory
#file -  the name of the file to be stored on the server
def STORE(file):
    #stores files to the server directory
    if os.path.isfile(file):
        ftp.storbinary('STOR '+ file, open(file, 'rb'))
        print("Sucessfully stored " + file)
    else:
        print("File does not exist")

#retrieves files from the server directory
#file_dl -  the name of the file to be retrieved from the server
def RETRIEVE(file_dl):
    if file_dl in ftp.nlst():
        for name, types in ftp.mlsd("",["type"]):
            if file_dl == name and types["type"] == 'dir':
                print("File is directory, cannot retrieve")
                return
        localfile = open(file_dl, 'wb')
        ftp.retrbinary('RETR ' + file_dl, localfile.write, 1024)

        localfile.close()
        print("Retrieved file " + file_dl)
    else:
        print("File wasn't found")
       
def main(): #creates a command line interface to connect with a given server and issue it commands
    quit = False
    connect = False
    while quit == False:
        command = input("Enter a command: ") #ask for input
        os.system('cls' if os.name == 'nt' else 'clear')#clears terminal output
        function = command.split(' ', 3) #splice the input into a list delimited by spaces
        if connect == False: #only allow the commands connect and quit when not connected to a server
            if function[0].upper() == "CONNECT":
                if len(function) == 3: # if the right number of parameters
                    if os.name == 'nt':
                        response = os.system("ping " + function[1]) #ping the server to see if it's on the network
                    else:
                    	response = os.system("ping -c 1 " + function[1]) #ping the server to see if it's on the network
                    if response == 0: #if ping successful
                        CONNECT(function[1], function[2])
                        connect = True
                    else:
                        print("IP address / Host name not valid, please try again")
                else:
                    usage_error(function[0])
            elif function[0].upper() == "QUIT":
                quit = True
            else:
                print("Need to connect to the server first!")
                print("Usage: CONNECT <server name/IP address> <server port>")
        else:
            if function[0].upper() == "RETRIEVE":
                if len(function) == 2:
                    RETRIEVE(function[1]) #retrieve file
                else:
                    usage_error(function[0])
            elif function[0].upper() == "STORE":
                if len(function) == 2:
                    STORE(function[1]) #store file
                else:
                    usage_error(function[0])
            elif function[0].upper() == "LIST":
                LIST() #list server directory
            elif function[0].upper() == "QUIT":
                ftp.close()
                quit = True
            elif function[0].upper() == "CONNECT":
            	print("Already connected to a server!")
            else:
                usage_error(function[0])
    print("Goodbye")
main() #call the main function
