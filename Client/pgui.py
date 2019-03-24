from tkinter import *
from tkinter import ttk
from functools import partial
import sys
import os
import socket
from ftplib import FTP

ftp = FTP('')

screen = Tk()
screen.title("GV-NAPSTER Host")
screen["bg"] = "lightgrey"
screen.resizable(0,0)

connFrame = LabelFrame(screen, text="Connection", bg = "lightgrey", width = 1000)
connFrame.grid(row = 0, column = 1, sticky = "W")
searchFrame = LabelFrame(screen, text="Search", bg = "lightgrey", width = 1000)
searchFrame.grid(row = 1, column = 1, sticky = "W")
ftpFrame = LabelFrame(screen, text="FTP", bg = "lightgrey", width = 1000)
ftpFrame.grid(row = 2, column = 1, sticky = "W")

shLabel = Label(connFrame, text="Server Hostname:", bg = "lightgrey")
shLabel.grid(row=0, column=1)
shText = Entry(connFrame, relief = GROOVE)
shText.grid(row=0, column=2)

portLabel = Label(connFrame, text="Port:", bg = "lightgrey")
portLabel.grid(row=0, column=3)
portText = Entry(connFrame, relief = GROOVE, width = 8)
portText.grid(row=0, column=4)

def connect():
	print(shText.get())
	shText.delete(0, END)

connectButton = Button(connFrame, text="Connect", width=10, command=connect)
connectButton.grid(row=0, column=5, padx = 10)

usrLabel = Label(connFrame, text="Username:", bg = "lightgrey")
usrLabel.grid(row=1, column=1)
usrText = Entry(connFrame, relief = GROOVE)
usrText.grid(row=1, column=2, pady = 10)

hostLabel = Label(connFrame, text="Hostname:", bg = "lightgrey")
hostLabel.grid(row=1, column=3)
hostText = Entry(connFrame, relief = GROOVE)
hostText.grid(row=1, column=4)

speedLabel = Label(connFrame, text="Speed:", bg = "lightgrey")
speedLabel.grid(row=1, column=5, padx = 0)

speedDropDown = StringVar(screen)
speedChoices = { 'Ethernet','Modem', 'T1', 'T3'}
speedDropDown.set('Ethernet') # set the default option

speedMenu = OptionMenu(connFrame, speedDropDown, *speedChoices)
speedMenu.grid(row = 1, column =6, padx = 0)

def change_dropdown(*args):
    print(speedDropDown.get())

speedDropDown.trace('w', change_dropdown)

kywordLabel = Label(searchFrame, text="Keyword:", bg = "lightgrey")
kywordLabel.grid(row=0, column=1)

kywordText = Entry(searchFrame, relief = GROOVE, width = 40)
kywordText.grid(row=0, column=2)

fileTree = ttk.Treeview(searchFrame, columns=("speed", "hostname", "filename", "description"))
fileTree['show'] = 'headings'
fileTree.column("speed", width = 80, anchor="center")
fileTree.column("hostname", width = 150, anchor="center")
fileTree.column("filename", width = 150, anchor="center")
fileTree.column("description", width = 250, anchor="center")
fileTree.heading('speed', text="Speed")
fileTree.heading('hostname', text="Hostname")
fileTree.heading('filename', text="Filename")
fileTree.heading('description', text="Description")
fileTree.grid(row = 1, column = 2)
fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))

def key_search():
	print(kywordText.get())
	kywordText.delete(0, END)
	fileTree.insert('', 'end', values=('Ethernet DaneMAC.local filename.txt "its file but its also a description" '))

searchButton = Button(searchFrame, text="Search", width=10, command=key_search)
searchButton.grid(row=0, column=3, padx = 10)

entcommLabel = Label(ftpFrame, text="Enter Command:", bg = "lightgrey")
entcommLabel.grid(row=0, column=1)

entcommText = Entry(ftpFrame, relief = GROOVE, width = 60)
entcommText.grid(row=0, column=2, pady = 10)

listbox = Listbox(ftpFrame, width = 70)
listbox.grid(row=1, column=2)


#Connects to the host server
#host - hostname / IP address of the server
#port - the port number (1026)
def CONNECT(host, port):
    ftp.connect(host, int(port))
    ftp.login()
    ftp.cwd('.') #replace with your directory
    ftp.retrlines('LIST')
    print("connected to " + host)

# listbox.insert(END, "Hello")
# listbox.insert(END, "HI")
def ftp_go(host, port):
	ftp.connect(host, int(port))
	ftp.login()
	ftp.cwd('.') #replace with your directory
	ftp.retrlines('LIST')
	print("connected to " + host)
	listbox.see(END)
	entcommText.delete(0, END)


goButton = Button(ftpFrame, text="Go", width=10, command=ftp_go)
goButton.grid(row=0, column=3, padx = 10)

screen.mainloop()
