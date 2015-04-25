#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import sqlite3 as lite
import Tkinter
from optparse import OptionParser
import sys
from PIL import Image, ImageTk

DB_NAME = "pyclinote.db"
con = None
title = 'pyGuiCliNote'
version = '1.1.0'
authors = 'tabuto83'
dateversion = '2015-04-25'

TEXT_NOTE=''
ID_NOTE=0
NOTE_LIST=False
DELETE_ALL=False
EDIT_NOTE=False
DELETE_NOTE=False
INSERT_NOTE=False
VERSION = False
GUI=False

QRY_S_TEST="SELECT name FROM sqlite_master WHERE type='table' AND name='note'"
QRY_C_NOTE="CREATE TABLE note(Id INT, noteText TEXT, priority INT, active INT)"
QRY_C_CONFIG="CREATE TABLE config(key TEXT, value TEXT)"
QRY_U_NOTE="UPDATE Note set noteText=? WHERE Id = ?"
QRY_U_PRIOR_PLUS="UPDATE Note set priority=priority+1 WHERE Id = ?"
QRY_U_PRIOR_MINUS="UPDATE Note set priority=priority-1 WHERE Id = ?"
QRY_U_ACTIVE_TOGGLE="UPDATE Note set active=1-active WHERE Id = ?"
QRY_D_ALL_NOTE="DELETE FROM Note WHERE Id = ?"
QRY_D_NOTE_BY_ID="DELETE FROM Note WHERE Id = ?"
QRY_S_NEXTVAL_NOTE="SELECT MAX(Id)+1 FROM note"
QRY_I_NOTE="INSERT INTO NOTE(Id,noteText,priority,active) VALUES(?,?,0,1)"
QRY_S_ALL_NOTE_RESUME="SELECT Id, substr(noteText,0,25) from note WHERE active=1 ORDER BY priority desc, Id desc"
QRY_S_NOTE_BY_ID="SELECT *  FROM Note WHERE Id = ?"
QRY_S_CONFGIG_BY_KEY = "SELECT value FROM config WHERE key = ? "
QRY_I_CONFIG = "INSERT INTO config(key,value) VALUES (?,?)"

def setNoteText(t):
	global TEXT_NOTE
	TEXT_NOTE=t
	
def setNoteId(i):
	global ID_NOTE
	ID_NOTE=i   

def insertConfig(cur,key,value):
	cur.execute(QRY_I_CONFIG,(key,value))
  
def getConnection():
	try:
		con = lite.connect(DB_NAME)
		
		cur = con.cursor()    
		cur.execute(QRY_S_TEST)
		
		data = cur.fetchone()
		
		#print "SQLite Table: %s" % data    
		if(data == None ):
			#creo tabella
			#if table not exist, create tables
			with con:
				cur = con.cursor()    
				cur.execute(QRY_C_NOTE)
				cur.execute(QRY_C_CONFIG)
				#add default configuration entry
				insertConfig(cur,"list.title","-- Note List -- ")
				insertConfig(cur,"preview.size","25")
				con.commit()
		return con            
    
	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)



def getConfig(key):
	if(not key):
		print "internal error: key not present, unable to load conf"
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_S_CONFGIG_BY_KEY,(key,))
	rows = cur.fetchall()
	row = rows[0]
	return row[0].encode('utf-8')

def editNote():
	if(not ID_NOTE or ID_NOTE<=0):
		parser.print_help()
		sys.exit(1)	
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_U_NOTE,(TEXT_NOTE,ID_NOTE))
	con.commit()
	return True
'''
With true increment priority, false decrement
'''
def incrementPriority(up=False):
	if(not ID_NOTE or ID_NOTE<=0):
		parser.print_help()
		sys.exit(1)	
	con = getConnection()
	cur = con.cursor()
	if(up):
		cur.execute(QRY_U_PRIOR_PLUS,(ID_NOTE,))
	else:
		cur.execute(QRY_U_PRIOR_MINUS,(ID_NOTE,))
	con.commit()
	return True

'''
Activate a disactive note or disactivate an active note
'''
def toggle():
	if(not ID_NOTE or ID_NOTE<=0):
		parser.print_help()
		sys.exit(1)	
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_U_ACTIVE_TOGGLE,(ID_NOTE,))

	con.commit()
	return True
		

def deleteAllNote():
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_D_ALL_NOTE)
	con.commit()
	return True

def deleteNote():
	if(not ID_NOTE or ID_NOTE<=0 ):
		parser.print_help()
		sys.exit(1)
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_D_NOTE_BY_ID,(ID_NOTE,))
	con.commit()
	return True

def insertNote():
	if(not TEXT_NOTE or len(TEXT_NOTE)<1 ):
		print TEXT_NOTE + "is not present" 
		parser.print_help()
		sys.exit(1)
	con = getConnection()
	cur = con.cursor()
	nextval = 0
	cur.execute(QRY_S_NEXTVAL_NOTE)
	fetchval = cur.fetchone()
	if(fetchval[0]):
		nextval= fetchval[0]
	else:
		nextval=1
	
	cur.execute(QRY_I_NOTE,(nextval,TEXT_NOTE))
	con.commit()
	return nextval
	
	

def getAllNotes():
	title = getConfig("list.title")
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_S_ALL_NOTE_RESUME)
	rows = cur.fetchall()
	result =title+"\n";
	for row in rows:
		result = result + str(row[0]) +'] '+ row[1].encode('utf-8')+"\n"
	
	print result
	return result

def getNoteTextById():
	if(not ID_NOTE or ID_NOTE<=0 ):
		parser.print_help()
		sys.exit(1)
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_S_NOTE_BY_ID,(ID_NOTE,))
	rows = cur.fetchall()
	row = rows[0]
	return row[1].encode('utf-8')

def credits():
	print "pyclinote: Pyhton Command Line Note Manager v"+version;
	print "Authors: "+authors;
	print dateversion

Lb1=None;
text=None;
textSelected=None;


def get_list(event):
	# get selected line index
	global ID_NOTE
	global Lb1
	global textSelected
	ID_NOTE = Lb1.curselection()[0]
	Lb1.activate(ID_NOTE)
	Lb1.select_set(ID_NOTE)
	#print ID_NOTE
	ID = Lb1.get(ID_NOTE)[:Lb1.get(ID_NOTE).index(']')]
	#TEXT = Lb1.get(ID_NOTE)[Lb1.get(ID_NOTE).index(']')+2:]
	
	#print ID
	ID_NOTE = int(ID)
	#retrieve all note text
	TEXT=getNoteTextById()
	#setting the text
	textSelected.config(state=NORMAL)
	textSelected.delete(1.0, END)
	textSelected.insert(INSERT, TEXT, "a")
	textSelected.config(state=DISABLED)
	#refreshNote()


def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

def addCallBack():
	global Lb1
	global text
	global TEXT_NOTE
	TEXT_NOTE=text.get("1.0",END);
	TEXT_NOTE=TEXT_NOTE[:len(TEXT_NOTE)-1]
	insertNote()
	TEXT_NOTE=''
	text.delete("1.0",END);
	refreshNote()

def delCallBack():
	deleteNote()
	refreshNote()

def plusCallBack():
	incrementPriority(True)
	refreshNote()

def minusCallBack():
	incrementPriority(False)
	refreshNote()

def toggleCallBack():
	toggle()
	refreshNote()

def clrCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

def refreshNote():
	global Lb1
	Lb1.delete(0, END)
	con = getConnection()
	cur = con.cursor()
	cur.execute(QRY_S_ALL_NOTE_RESUME)
	rows = cur.fetchall()
	for row in rows:
		Lb1.insert(row[0],str(row[0]) +'] '+row[1])


#GUI
def gui():
	global Lb1
	global text
	global textSelected
	top = Tkinter.Tk()
	top.wm_title(title+" v."+version )
	# Code to add widgets will go here...
	
	#TOOLBAR
	toolbar = Frame(top, bd=1, relief=RAISED)
	img = Image.open("note_add.png")
	eimg = ImageTk.PhotoImage(img)  
	addButton = Button(toolbar, image=eimg, relief=FLAT,command=addCallBack)
	addButton.image = eimg
	addButton.pack(side=LEFT, padx=2, pady=2)
	
	delImg = Image.open("delete.png")
	delEimg = ImageTk.PhotoImage(delImg) 
	delButton = Button(toolbar, image=delEimg, relief=FLAT,command=delCallBack)
	delButton.image = delEimg
	delButton.pack(side=LEFT, padx=2, pady=2)
	
	toggleImg = Image.open("deactivate.png")
	toggleEimg = ImageTk.PhotoImage(toggleImg) 
	toggleButton = Button(toolbar, image=toggleEimg, relief=FLAT,command=toggleCallBack)
	toggleButton.image = toggleEimg
	toggleButton.pack(side=LEFT, padx=2, pady=2)
	
	upImg = Image.open("navigate-up.png")
	upEimg = ImageTk.PhotoImage(upImg) 
	upButton = Button(toolbar, image=upEimg, relief=FLAT,command=plusCallBack)
	upButton.image = upEimg
	upButton.pack(side=LEFT, padx=2, pady=2)
	
	downImg = Image.open("navigate-down.png")
	downEimg = ImageTk.PhotoImage(downImg) 
	downButton = Button(toolbar, image=downEimg, relief=FLAT,command=minusCallBack)
	downButton.image = downEimg
	downButton.pack(side=LEFT, padx=2, pady=2)
	
	
	scrollbar = Scrollbar(top)
	Lb1 = Listbox(top,yscrollcommand = scrollbar.set)
	text = Text(top,height=10)
	textSelected = Text(top,height=10)
	textSelected.config(state=DISABLED)
	
	#btn_add = Tkinter.Button(top, text ="Add", command = addCallBack)
	#btn_del = Tkinter.Button(top, text ="Delete", command = delCallBack)
	#btn_clr = Tkinter.Button(top, text ="Clear", command = helloCallBack)
	
	#btn_prior_plus = Tkinter.Button(top, text ="+", command = plusCallBack)
	#btn_prior_minus = Tkinter.Button(top, text ="-", command = minusCallBack)
	
	refreshNote()
	'''
	con = getConnection()
	cur = con.cursor()
	cur.execute("SELECT * from note")
	rows = cur.fetchall()
	for row in rows:
		Lb1.insert(row[0], row[1])
	'''
	#Lb1.pack()
	#text.pack()
	#btn_add.pack()
	#btn_del.pack()
	
	toolbar.grid(row=0,column=0, columnspan=3)
	
	listLabel = Label(top, text="Note List")
	textSelectedLabel = Label(top, text="Selected Note Text")
	textLabel = Label(top, text="New Note Text")
	
	
	
	listLabel.grid(row=1,column=0)
	
	Lb1.grid(row=2,column=0,sticky=N+E+S+W)
	scrollbar.grid(row=2,column=1,sticky=N+S )
	#btn_prior_plus.grid(row=1,column=2,sticky=N+W)
	#btn_prior_minus.grid(row=2,column=2,sticky=N+W)
	
	scrollbar.config( command = Lb1.yview )
	textSelectedLabel.grid(row=3,column=0)
	textSelected.grid(row=4,column=0,columnspan=3)
	textLabel.grid(row=5,column=0)
	text.grid(row=6,column=0,columnspan=3)
	#btn_add.grid(row=6,column=0)
	#btn_del.grid(row=6,column=1)
	#btn_clr.grid(row=6,column=2)
	#Lb1.bind('<ButtonRelease-1>', get_list)
	Lb1.bind('<<ListboxSelect>>', get_list)
	top.mainloop()

def entry_point():
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-i", "--insert",action="store_true", dest="INSERT_NOTE",help="insert new note")
	parser.add_option("-e", "--edit",action="store_true", dest="EDIT_NOTE", help="edit note")
	parser.add_option("-d", "--delete",action="store_true", dest="DELETE_NOTE", help="delete single note")
	parser.add_option("-c", "--clear",action="store_true", dest="DELETE_ALL", help="delete all notes")
	parser.add_option("-s", "--show",action="store_true", dest="NOTE_LIST", help="show all notes")
	parser.add_option("-g", "--gui",action="store_true", dest="GUI", help="show GUI")
	parser.add_option("-v", "--version",action="store_true", dest="VERSION", help="show all notes")



	parser.add_option("-t", "--text",action="store", type="string", dest="TEXT_NOTE",help="note text")
	parser.add_option("-r", "--rowid",action="store", type="int", dest="ID_NOTE",help="note text")


	#init()
	#getAllNotes()
	#deleteAllNote()
	#getAllNotes()
	#insertNote("Nuova nota");
	#getAllNotes()
	#editNote(100,'tette grasse')
	#getAllNotes()
	(options, args) = parser.parse_args();
	TEXT_NOTE=options.TEXT_NOTE
	ID_NOTE=options.ID_NOTE

	NOTE_LIST=options.NOTE_LIST
	DELETE_ALL=options.DELETE_ALL
	EDIT_NOTE=options.EDIT_NOTE
	DELETE_NOTE=options.DELETE_NOTE
	INSERT_NOTE=options.INSERT_NOTE
	GUI=options.GUI
	VERSION=options.VERSION
	'''
	print TEXT_NOTE
	print ID_NOTE

	print NOTE_LIST
	print DELETE_ALL
	print EDIT_NOTE
	print DELETE_NOTE
	print INSERT_NOTE
	'''
	if(INSERT_NOTE):
		insertNote()
	elif (DELETE_NOTE):
		deleteNote()
	elif (DELETE_ALL):
		deleteAllNote()
	elif (NOTE_LIST):
		getAllNotes()
	elif (EDIT_NOTE):
		editNote()
	elif(VERSION):
		credits()
	elif(GUI):
		gui()
	else:
		parser.print_help()
		sys.exit(1)


def main():
    pass

if __name__ == "__main__":
	entry_point()

