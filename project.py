import os
import win32gui, win32con
from time import sleep
import sqlite3
import project_functions

# Clear Screen Function
def clear(time=0):
  sleep(time)
  os.system('cls')

# Define Employee View of Database Application
def Employee(conn,cursor,lib):
  clear()
  flag = True
  while flag:
    # Menu of Possible Actions
    print("Library Managment System".center(60,"-"),end="\n\n")
    print("[1] Add Inventory Item".ljust(30),end='')
    print("[2] Remove Inventory Item")
    print("[3] Add New Employee or Member".ljust(30),end='')
    print("[4] Remove Employee or Member")
    print("[5] Search for Book".ljust(30),end='')
    print("[6] Search for Movie")
    print("[7] Search for Item Borrower".ljust(30),end='')
    print("[8] Search for Borrowed Items")
    print("[9] Check Out Item".ljust(30),end='')
    print("[10] Check In Item")
    print("[11] Generate a Report".ljust(30),end='')
    print("[0] Return")
    print()
    
    # Perform Selected Action
    menu = int(input())
    clear()
    if menu == 0:
      flag = False
    elif menu == 1:
      project_functions.Add_Inv(conn,cursor,lib) 
    elif menu == 2:
      project_functions.Rem_Inv(conn,cursor)
    elif menu == 3:
      project_functions.Add_Person(conn,cursor,lib)
    elif menu == 4:
      project_functions.Rem_Person(conn,cursor)
    elif menu == 5:
      project_functions.Query_for_Book(cursor,lib)
    elif menu == 6:
      project_functions.Query_for_Movie(cursor,lib)
    elif menu == 7:
      project_functions.Query_for_Borrower(cursor,lib)
    elif menu == 8:
      project_functions.Query_for_Borrowed_Items(cursor,lib)
    elif menu == 9:
      project_functions.Check_Out_Item(conn,cursor,lib)
    elif menu == 10:
      project_functions.Check_In_Item(conn,cursor,lib)
    elif menu == 11:
      project_functions.Generate_Report(cursor,lib)
    
    clear()

# Define Member View of Databse Application
def Member(conn,cursor,lib,mem):
  clear()
  flag = True
  while flag:
    # Menu of Possible Actions
    print("Library Search System".center(60,"-"),end="\n\n")
    print("[1] Search for Book".ljust(30),end='')
    print("[2] Search for Movie")
    print("[3] Search for Borrowed Items".ljust(30),end='')
    print("[4] Check Out Item")
    print("[5] Check In Item".ljust(30),end='')
    print("[0] Return")
    print()
    
    # Perform Selected Action
    menu = int(input())
    clear()
    if menu == 0:
      flag = False
    elif menu == 1:
      project_functions.Query_for_Book(cursor,lib)
    elif menu == 2:
      project_functions.Query_for_Movie(cursor,lib)
    elif menu == 3:
      project_functions.Query_for_Borrowed_Items(cursor,lib,mem)
    elif menu == 4:
      project_functions.Check_Out_Item(conn,cursor,lib,mem)
    elif menu == 5:
      project_functions.Check_In_Item(conn,cursor,lib,mem)
    
    clear()

# Adjust console size
hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
os.system('mode con: cols=200 lines=200')

# Clear Screen
clear()

# Path to SQL File
sql_file_path = 'project.sql'

# Connect to the SQLite database
conn = sqlite3.connect('project.db')
cursor = conn.cursor()

# Enable Foreign Key Constraint
conn.setconfig(sqlite3.SQLITE_DBCONFIG_ENABLE_FKEY,True)

# Open and read the SQL file if database is new
res = cursor.execute("SELECT name FROM sqlite_master")
if(len(res.fetchall()) == 0):
  with open(sql_file_path, 'r') as sql_file:
    sql_script = sql_file.read()

  # Execute the SQL script if database is new
  cursor.executescript(sql_script)

  # Commit the changes and close the connection if database is new
  conn.commit()

# Main Application Body
flag = True
while flag:
  login,lib,mem = project_functions.Login(cursor)
  if login == 0:
    flag = False
  elif login == -1:
    Employee(conn,cursor,lib)
  elif login == 1:
    Member(conn,cursor,lib,mem)
  clear()

# Close Cursor and Connection
cursor.close()
conn.close()

# Clear Screen
clear()