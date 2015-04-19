# pyclinote
A simple (one file) command line note manager with python2.7 and SQLite

Simple to use:

Python2.7 and tkinter library required!

Copy file in a directory.
Launch file with python pyclinote.py wil show command line options:

Options:

    -h, --help            show this help message and exit
  
    -i, --insert          insert new note
  
    -e, --edit            edit note
  
    -d, --delete          delete single note
  
    -c, --clear           delete all notes
  
    -s, --show            show all notes
  
    -g, --gui             show GUI
  
    -v, --version         show all notes
  
    -t TEXT_NOTE, --text=TEXT_NOTE note text
  
    -r ID_NOTE, --rowid=ID_NOTE note text
  

Examples:

Insert a note:

    python pyclinote.py -i -t "New Note"
 
 
Show All Note will show Note Id and Note Text

    python pyclinote.py -s
 
Output:

    -- Note List -- 
    1] New Note

Edit a note:

    python pyclinote.py -e -r 1 -t "Note edited"
    
-r 1 means that you want edited note with id=1

Delete a note with id=1:

    python pyclinote.py -d -r 1

Delete all note (clear):

    python pyclinote.py -c


Show a simple GUI to perform basic actions:

    python pyclinote.py -g
    

Here (http://b-admin.blogspot.it/2015/04/show-and-manage-notes-on-your-linux.html)  can find how use pyclinote to show notes on desktop using conky

That's all!



