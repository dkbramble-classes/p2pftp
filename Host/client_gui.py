#Authors: Luke Bassett, Dane Bramble, Patrik Kozak, Brendan Warnick
#This is a Client/Server program that contain
from tkinter import * #Importation of the GUI objects
from tkinter import ttk #Allows for the Treeview object
import local_server
import threading

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

#When the "Connect" button is clicked, this function take the text input fields and uses them to connect to the centralized server
def connect():
	print(shText.get()) #get the value of the text box
	shText.delete(0, END) # delete text in the text box

#Connect button
connectButton = Button(connFrame, text="Connect", width=10, command=connect)
connectButton.grid(row=0, column=5, padx = 10)

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

speedDropDown.trace('w', change_dropdown) #set the function to cisciscisicisicisicisicisicisicisicisciisicsicisicisicisiicisiciicsicisicisicisicisii

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
fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))
fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))
fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))
fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))

#This function takes the input and searches the server for possible filenames.
#The results of the search are returned into the fileTree table
def key_search():
	print(kywordText.get())
	kywordText.delete(0, END)
	#fileTree.delete(*fileTree.get_children()) # delete all entries of the grid
	fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))
	fileTree.insert('', 'end', values=('hello DaneMAC.local filename.txt "its file but its also a description" '))
	fileTree.insert('', 'end', values=('hi DaneMAC.local filename.txt "its file ccccccccccccccccccccccccbut its also a description" '))

#Search Button position
searchButton = Button(searchFrame, text="Search", width=10, command=key_search) #specify which function is called on click
searchButton.grid(row=0, column=3, padx = 10)

#Enter Command text box and label
entcommLabel = Label(ftpFrame, text="Enter Command:", bg = "lightgrey")
entcommLabel.grid(row=0, column=1)
entcommText = Entry(ftpFrame, relief = GROOVE, width = 60)
entcommText.grid(row=0, column=2, pady = 10)

#listbox keeps track of commands made and any communications between the hosts
listbox = Listbox(ftpFrame, width = 70)
listbox.grid(row=1, column=2)

#Example of inserting into listbox
# listbox.insert(END, "Hello")
# listbox.insert(END, "HI")

#This function executes any command entered into the Enter Command text box
def ftp_go():
	listbox.see(END)
	entcommText.delete(0, END)

goButton = Button(ftpFrame, text="Go", width=10, command=ftp_go)
goButton.grid(row=0, column=3, padx = 10)

#This is responsible for the gui remaining open. This will end when the window is closed
screen.mainloop()
