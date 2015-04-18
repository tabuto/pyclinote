#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import sqlite3 as lite
import Tkinter
from optparse import OptionParser
import sys

con = None
title = 'pyGuiCliNote'
version = '1.0.0'
authors = 'tabuto83'
dateversion = '2015-16-04'

TEXT_NOTE=''
ID_NOTE=0
NOTE_LIST=False
DELETE_ALL=False
EDIT_NOTE=False
DELETE_NOTE=False
INSERT_NOTE=False
VERSION = False
GUI=False
    
def getConnection():
	try:
		con = lite.connect('test.db')
		
		cur = con.cursor()    
		cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='note'")
		
		data = cur.fetchone()
		
		#print "SQLite Table: %s" % data    
		if(data == None ):
			#creo tabella
			#Tabella non presente, creo la tabella
			with con:
				cur = con.cursor()    
				cur.execute("CREATE TABLE note(Id INT, noteText TEXT)")
		return con            
    
	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

#obsoleto
def init():
	#check db
	global con
	try:
		con = lite.connect('test.db')
		
		cur = con.cursor()    
		cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='note'")
		
		data = cur.fetchone()
		
		print "SQLite Table: %s" % data    
		if(data == None ):
			#creo tabella
			with con:
				cur = con.cursor()    
				cur.execute("CREATE TABLE note(Id INT, noteText TEXT)")            
    
	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
		

def editNote():
	if(not ID_NOTE or ID_NOTE<=0 or not TEXT_NOTE or len(TEXT_NOTE)<1 ):
		parser.print_help()
		sys.exit(1)
		
	con = getConnection()
	cur = con.cursor()
	cur.execute("UPDATE Note set noteText=? WHERE Id = ?",(TEXT_NOTE,ID_NOTE))
	con.commit()

def deleteAllNote():
	con = getConnection()
	cur = con.cursor()
	cur.execute("DELETE FROM Note ")
	con.commit()

def deleteNote():
	if(not ID_NOTE or ID_NOTE<=0 ):
		parser.print_help()
		sys.exit(1)
	con = getConnection()
	cur = con.cursor()
	cur.execute("DELETE FROM Note WHERE Id = ?",(ID_NOTE,))
	con.commit()

def insertNote():
	if(not TEXT_NOTE or len(TEXT_NOTE)<1 ):
		parser.print_help()
		sys.exit(1)
	con = getConnection()
	cur = con.cursor()
	nextval = 0
	cur.execute("SELECT MAX(Id)+1 FROM note")
	fetchval = cur.fetchone()
	if(fetchval[0]):
		nextval= fetchval[0]
	else:
		nextval=1
	
	cur.execute("INSERT INTO NOTE(Id,noteText) VALUES(?,?)",(nextval,TEXT_NOTE))
	con.commit()
	#cur.execute("INSERT INTO NOTE VALUES("+str(nextval)+",'"+note+"')")
	

def getAllNotes():
	print "-- Note List -- "
	con = getConnection()
	cur = con.cursor()
	cur.execute("SELECT * from note")
	rows = cur.fetchall()
	for row in rows:
		print str(row[0]) +'] '+ row[1].encode('utf-8')

def credits():
	print "pyclinote: Pyhton Command Line Note Manager v"+version;
	print "Authors: "+authors;
	print dateversion

Lb1=None;
text=None;


def get_list(event):
	# get selected line index
	global ID_NOTE
	global Lb1
	ID_NOTE = Lb1.curselection()[0]
	Lb1.activate(ID_NOTE)
	Lb1.select_set(ID_NOTE)
	#print ID_NOTE
	ID = Lb1.get(ID_NOTE)[:Lb1.get(ID_NOTE).index(']')]
	#print ID
	ID_NOTE = int(ID)
	
	refreshNote()


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

def clrCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

def refreshNote():
	global Lb1
	Lb1.delete(0, END)
	con = getConnection()
	cur = con.cursor()
	cur.execute("SELECT * from note")
	rows = cur.fetchall()
	for row in rows:
		Lb1.insert(row[0],str(row[0]) +'] '+row[1])

#GUI
def gui():
	global Lb1
	global text
	top = Tkinter.Tk()
	top.wm_title(title+" v."+version )
	# Code to add widgets will go here...
	scrollbar = Scrollbar(top)
	Lb1 = Listbox(top,yscrollcommand = scrollbar.set)
	text = Text(top)
	btn_add = Tkinter.Button(top, text ="Add", command = addCallBack)
	btn_del = Tkinter.Button(top, text ="Delete", command = delCallBack)
	btn_clr = Tkinter.Button(top, text ="Clear", command = helloCallBack)
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
	listLabel = Label(top, text="Note List")
	textLabel = Label(top, text="Note Text")
	
	
	
	listLabel.grid(row=0,column=0)
	
	Lb1.grid(row=1,column=0,sticky=N+E+S+W)
	scrollbar.grid(row=1,column=1,sticky=N+S )
	scrollbar.config( command = Lb1.yview )
	textLabel.grid(row=2,column=0)
	text.grid(row=3,column=0,columnspan=3)
	btn_add.grid(row=4,column=0)
	btn_del.grid(row=4,column=1)
	btn_clr.grid(row=4,column=2)
	Lb1.bind('<ButtonRelease-1>', get_list)
	top.mainloop()

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




