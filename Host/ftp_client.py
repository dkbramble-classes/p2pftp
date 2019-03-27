#This is a client program to connect with a multithreaded server using pyftpdlib. See requirements.txt for usage
#Authors: Luke Bassett, Dane Bramble, Patrik Kozak, Brendan Warnick
#Project for CIS 457
#Last Edited: February 9, 2019
#current ideas from https://www.techinfected.net/2017/07/create-simple-ftp-server-client-in-python.html
import sys
import os
import socket
from ftplib import FTP

ftp = FTP('')

def usage_error(cmd): #error message that prints out the usage of the client
    if cmd != '':
        print("improper usage of '" + cmd + "\'")
    print("Commands: \n\t CONNECT <server name/IP address> <server port> \n\t LIST \n\t RETRIEVE <filename> \n\t STORE <filename> \n\t QUIT")

def Connect():
    ftp.connect(function[1],function[2])
    ftp.login()
    ftp.cwd('.') #replace with your directory


def LIST():
    #retrieves a list of files from the directory: ~/Documents
    ftp.retrlines('LIST')

def RETRIEVE(file_dl):

    localfile = open(file_dl, 'wb')
    ftp.retrbinary('RETR ' + file_dl, localfile.write, 1024)

    localfile.close()
       
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
                    response = os.system("ping -c 1 " + function[1]) #ping the server to see if it's on the network
                    if response == 0: #if ping successful
                        ftp.connect(function[1],int(function[2]))
                        ftp.login()
                        ftp.cwd('.') #replace with your directory
                        ftp.retrlines('LIST')
                        connect = True
                        print("connected to " + function[1])
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
                    RETRIEVE(function[1])
                else:
                    usage_error(function[0])
            elif function[0].upper() == "STORE":
                if len(function) == 2:
                    print(function[1])
                else:
                    usage_error(function[0])
            elif function[0].upper() == "LIST":
                LIST()
            elif function[0].upper() == "QUIT":
                ftp.close()
                quit = True
            else:
                usage_error(function[0])
    print("Goodbye")
main() #call the main function
