#Authors: Luke Bassett, Dane Bramble, Patrik Kozak, Brendan Warnick
#This is a Client/Server program that contain
from tkinter import * #Importation of the GUI objects
from tkinter import ttk #Allows for the Treeview object
import local_server
import threading
import sys
import os
import socket
from ftplib import FTP
import json
import requests

quitURL = ""
quitUser = ""
ftp = FTP(timeout = 2)
connectFlag = False
lines = []
connected = False

host_server = local_server.ftp_server()
srv = threading.Thread(target=host_server.run, daemon=True)
srv.start()

#Main window screen
screen = Tk()
screen.title("GV-NAPSTER Host")
screen["bg"] = "lightgrey"
screen.resizable(0,0) #locks the frame from growing/shrinking

#Menu subsections
connFrame = LabelFrame(screen, text="Connection", bg = "lightgrey", width = 1000)
connFrame.grid(row = 0, column = 1, sticky = "W")
searchFrame = LabelFrame(screen, text="Search", bg = "lightgrey", width = 1000)
searchFrame.grid(row = 1, column = 1, sticky = "W")
ftpFrame = LabelFrame(screen, text="FTP", bg = "lightgrey", width = 1000)
ftpFrame.grid(row = 2, column = 1, sticky = "W")

#Server Hostname text box and labels
shLabel = Label(connFrame, text="Server Hostname:", bg = "lightgrey")
shLabel.grid(row=0, column=1) #set position within the menu subsection
shText = Entry(connFrame, relief = GROOVE) #text box creation
shText.grid(row=0, column=2)

#Port Number text box and label
portLabel = Label(connFrame, text="Port:", bg = "lightgrey")
portLabel.grid(row=0, column=3)
portText = Entry(connFrame, relief = GROOVE, width = 8)
portText.grid(row=0, column=4)


#Username text box and labels
usrLabel = Label(connFrame, text="Username:", bg = "lightgrey")
usrLabel.grid(row=1, column=1)
usrText = Entry(connFrame, relief = GROOVE)
usrText.grid(row=1, column=2, pady = 10)

#Hostname text box and labels
hostLabel = Label(connFrame, text="Hostname:", bg = "lightgrey")
hostLabel.grid(row=1, column=3)
hostText = Entry(connFrame, relief = GROOVE)
hostText.grid(row=1, column=4)

#Speed drop down options and labels
speedLabel = Label(connFrame, text="Speed:", bg = "lightgrey")
speedLabel.grid(row=1, column=5, padx = 0)

speedDropDown = StringVar(screen)
speedChoices = { 'Ethernet','Modem', 'T1', 'T3'} #populate options for drop down
speedDropDown.set('Ethernet') # set the default option

speedMenu = OptionMenu(connFrame, speedDropDown, *speedChoices) #Drop down instantiation in menu
speedMenu.grid(row = 1, column =6, padx = 0)

#This function is applied whenever the drop down menu has changed
def change_dropdown(*args):
    print(speedDropDown.get())

speedDropDown.trace('w', change_dropdown) #set the function to

#When the "Connect" button is clicked, this function take the text input fields and uses them to connect to the centralized server
def connectTime():
	global connected
	if not connected:
		if shText.get() != "" and usrText.get() != "" and portText.get() != "" and hostText.get() != "" and speedDropDown.get() != "":
			URL = "http://" + shText.get()
			connectInput = "User_" + usrText.get() + "_" + hostText.get() + "_" + speedDropDown.get()
			try:
				r = requests.post(URL, data=connectInput)
				print(r.text)
				if r.text == "CONNECTED":
					try:
						connected = True
						global quitURL
						global quitUser
						quitURL = URL
						quitUser = usrText.get()
						with open('./file_descriptions.txt', 'r') as myfile:
							data=myfile.read().replace('\n', '')
						input = "File_" + usrText.get() + "_" + data
						q = requests.post(URL, data=input)
						print("The response is: " + q.text)
						#User_username_hostname_connection
						#jstring = json.loads(data)
						#curl -d input
			    		# Store configuration file values
					except FileNotFoundError:
						print("Issue uploading file descriptions")
			except requests.exceptions.ConnectionError:
				print("Couldn't connect to Centralized Server")
	else:
		print("You're already connected to a server!")


#Connect button
connectButton = Button(connFrame, text="Connect", width=10, command=connectTime)
connectButton.grid(row=0, column=5, padx = 10)

#Keyword text box and label
kywordLabel = Label(searchFrame, text="Keyword:", bg = "lightgrey")
kywordLabel.grid(row=0, column=1)
kywordText = Entry(searchFrame, relief = GROOVE, width = 40)
kywordText.grid(row=0, column=2)

#File List Result table
fileTree = ttk.Treeview(searchFrame, columns=("speed", "hostname", "filename", "description")) #how many columns in table
fileTree['show'] = 'headings' #remove first column
#Set widths for each column
fileTree.column("speed", width = 80, anchor="center")
fileTree.column("hostname", width = 150, anchor="center")
fileTree.column("filename", width = 150, anchor="center")
fileTree.column("description", width = 250, anchor="center")
#Set header name for each column
fileTree.heading('speed', text="Speed")
fileTree.heading('hostname', text="Hostname")
fileTree.heading('filename', text="Filename")
fileTree.heading('description', text="Description")
fileTree.grid(row = 1, column = 2)
#Insert values into table, values are seperated by space, use "" if it is one item

#This function takes the input and searches the server for possible filenames.
#The results of the search are returned into the fileTree table
#This function takes the input and searches the server for possible filenames.
#The results of the search are returned into the fileTree table
def key_search():
	# defining a params dict for the parameters to be sent to the API
	# PARAMS = {'search':kywordText.get()}
	fileTree.delete(*fileTree.get_children()) # delete all entries of the grid

	url = "http://" + shText.get() + "/?search=" + kywordText.get()

# sending get request and saving the response as response object
	r = requests.get(url)
	print(r.text)
	datastore = json.loads(r.text)
	for value in datastore:
		desc = "\ ".join(datastore[value]['description'].split(' '))
		fileTree.insert('', 'end', values=(datastore[value]['connection'] + ' ' + datastore[value]['hostname'] + ' ' + datastore[value]['file'] + ' ' + desc ))
	#data = r.json()
	kywordText.delete(0, END)

	# fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))
	# fileTree.insert('', 'end', values=('hello DaneMAC.local filename.txt "its file but its also a description" '))
	# fileTree.insert('', 'end', values=('hi DaneMAC.local filename.txt "its file ccccccccccccccccccccccccbut its also a description" '))

#Search Button position
searchButton = Button(searchFrame, text="Search", width=10, command=key_search) #specify which function is called on click
searchButton.grid(row=0, column=3, padx = 10)

#Enter Command text box and label
entcommLabel = Label(ftpFrame, text="Enter Command:", bg = "lightgrey")
entcommLabel.grid(row=0, column=1)
entcommText = Entry(ftpFrame, relief = GROOVE, width = 60)
entcommText.grid(row=0, column=2, pady = 10)

#listbox keeps track of commands made and any communications between the hosts
listbox = Listbox(ftpFrame, width = 90)
listbox.grid(row=1, column=2)

#Appends each line in the list "Lines"
def append_line(line):
    lines.append(line)

#Connects user to ftp_server
def CONNECT(host, port):
	try:
		ftp.connect(host, int(port))
		ftp.login()
		ftp.cwd('.') #replace with your directory
		listbox.insert(END, entcommText.get())
		conOutput = str("connected to " + host + " " + port)
		listbox.insert(END, conOutput)
		connectFlag = True
		listbox.see(END)
	except:
		listbox.insert(END, "connection to " + host + "\'s timed out, please try again later")
		listbox.see(END)

#Allows the user to view a list of the files on the ftp_server
def LIST():
	global connectFlag
	try:
		ftp.retrlines('NLST', append_line)
		for i in lines:
			listbox.insert(END, i)
		listbox.see(END)
	except EOFError:
		nonList = str("Server has cut connections with all hosts, cannot view files")
		listbox.insert(END, nonList)
		connectFlag = False


#stores files to the server directory
#file -  the name of the file to be stored on the server
def STORE(file):
	#stores files to the server directory
	global connectFlag
	try:
		ftp.size("dummyfile.txt")
		if os.path.isfile(file):
				ftp.storbinary('STOR '+ file, open(file, 'rb'))
				storeFile = str("Sucessfully stored " + file)
				listbox.insert(END, storeFile)
				listbox.see(END)
		else:
			storeFail = str("File does not exist")
			listbox.insert(END, storeFail)
	except:
		nonStore = str("Server has cut connections with all hosts, cannot store a file")
		listbox.insert(END, nonStore)
		connectFlag = False





#retrieves files from the server directory
#file_dl -  the name of the file to be retrieved from the server
def RETRIEVE(file_dl):
	global connectFlag
	try:
		if file_dl in ftp.nlst():
		    for name, types in ftp.mlsd("",["type"]):
		        if file_dl == name and types["type"] == 'dir':
		            retrDir = str("File is directory, cannot retrieve")
		            listbox.insert(END, retrDir)
		            return
		    localfile = open(file_dl, 'wb')
		    ftp.retrbinary('RETR ' + file_dl, localfile.write, 1024)

		    localfile.close()
		    retrOutput = str("Retrieved file " + file_dl)
		    listbox.insert(END, retrOutput)
		    listbox.see(END)
		else:
		    retrFail = str("File wasn't found")
		    listbox.insert(END, retrFail)
		    listbox.see(END)
	except BrokenPipeError:
		nonRetr = str("Server has cut connections with all hosts, cannot retrieve a file")
		listbox.insert(END, nonRetr)
		connectFlag = False

def usage_error(cmd):
    if cmd != '':
        listbox.insert(END, "improper usage of '" + cmd + "\'")
    listbox.insert(END, "Commands: \n\t CONNECT <server name/IP address> <server port> \n\t LIST \n\t RETRIEVE <filename> \n\t STORE <filename> \n\t QUIT")

#This function executes any command entered into the Enter Command text box
def ftp_go():
	global lines
	lines = []
	global connectFlag
	listbox.delete(0, END)
	#quit = False
	#while quit == False:
	command = entcommText.get()
	os.system('cls' if os.name == 'nt' else 'clear')#clears terminal output
	function = command.split(' ', 3) #splice the input into a list delimited by spaces
	if connectFlag == False: #only allow the commands connect and quit when not connected to a server
		if function[0].upper() == "CONNECT":
			if len(function) == 3: # if the right number of parameters
				if os.name == 'nt':
					response = os.system("ping " + function[1]) #ping the server to see if it's on the network
				else:
					response = os.system("ping -c 1 " + function[1]) #ping the server to see if it's on the network
				if response == 0: #if ping successful
					CONNECT(function[1], function[2])
					connectFlag = True
				else:
					listbox.insert(END, "IP address / Host name not valid, please try again")
					listbox.see(END)
					#print("IP address / Host name not valid, please try again")
			else:
				usage_error(function[0])
		elif function[0].upper() == "QUIT":
			quit = True
		else:
			listbox.insert(END, "Need to connect to the server first!")
			listbox.insert(END, "Usage: CONNECT <server name/IP address> <server port>")
			listbox.see(END)
			#print("Need to connect to the server first!")
			#print("Usage: CONNECT <server name/IP address> <server port>")
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
			connectFlag = False
			listbox.insert(END, "Disconnected from server")
		elif function[0].upper() == "CONNECT":
			listbox.insert(END, "Already connected to a server!")
			listbox.see(END)
			#print("Already connected to a server!")
		else:
			usage_error(function[0])

	entcommText.delete(0, END)

goButton = Button(ftpFrame, text="Go", width=10, command=ftp_go)
goButton.grid(row=0, column=3, padx = 10)

#This is responsible for the gui remaining open. This will end when the window is closed
screen.mainloop()

if connected:
	input = "Quit_" + quitUser

	r = requests.post(quitURL, data=input)
	if r.text == "DELETED":
		print("Sucessfully disconnected")