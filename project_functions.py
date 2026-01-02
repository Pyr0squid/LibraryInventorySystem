import os
from time import sleep

# Clear Screen
def clear(time=0):
  sleep(time)
  os.system('cls')

# Prints Table Format given a list of tuples and cursor object
def Print_Table(cursor,table):
  print("|",end="")
  it = 0
  for i in cursor.description:    
    print(i[0].center(22),end='')
    print("|",end="")
    it = it + 1
  print()

  print("".center(it*23+1,"-"))

  for i in table:
    print("|",end="")
    for j in i:
      print(str(j).center(22),end="")
      print("|",end="")
    print()

# Function that allows Employee to access Employee only view; Returns False if not Employee and True if Employee
def Emp_Login(username,password,cursor):
  # determine if username belongs to an employee
  emp_flag = False
  res = cursor.execute("SELECT Fname,Lname,Ssn,Libname FROM Employee")
  for i in res.fetchall():
    if username == i[0][:3] + i[1][:3]:
        emp_flag = True
        employee = i[2]
        lib = i[3]
  
  if emp_flag == True:
    # determine if password matches one on file
    pass_flag = False
    res = cursor.execute("SELECT Password FROM Employee WHERE Ssn = ?",[employee])
    if password == res.fetchone()[0]:
      pass_flag = True
  
  # If username or password is incorrect, print message and return False; else return True
  if (not emp_flag) or (not pass_flag):
    print("Username or Password Incorrect")
    clear(1)
    return False, None
  else:
    return True, lib
  
# Function that gives Members access to Member view; returns True if Member and False otherwise
def Mem_Login(id,cursor):
  # determine if id belongs to a member
  mem_flag = False
  res = cursor.execute("SELECT LibID,Libname FROM Member")
  for i in res:
    if id == i[0]:
      mem_flag = True
      member = i[1]
  
  # if member id does not exist, print message and returns false, otherwise returns true
  if not mem_flag:
    print("Library ID Incorrect")
    member = None
    clear(1)
  return mem_flag, member,id

# Function combines Emp_Login and Mem_Login; returns -1 for Employee, 1 for Member, and 0 for exit
def Login(cursor):
  while True:
    menu = int(input("[1] Employee Login\n[2] Member Login\n[0] Exit\n"))
    clear()
    if menu == 1:
      flag,lib = Emp_Login(input("Guest Login: addmin, admin\nEnter Username: "),input("Enter Password: "),cursor)
      if flag:
        return -1,lib,None
    elif menu == 2:
      flag,lib,mem = Mem_Login(int(input("Enter Library ID: ")),cursor)
      if flag:
        return 1,lib,mem
    elif menu == 0:
      return 0,None,None
    else:
      clear()

# Function adds a new inventory item to the Inventory Table and the Book/Movie Table
def Add_Inv(conn,cursor,lib):
  flag = True
  while flag:
    menu = int(input("[1] Add Book\n[2] Add Movie\n[0] Return\n"))
    clear()
    
    if menu == 1:
      id = int(input("Enter Inventory Number: "))
      try:
        cursor.execute("INSERT INTO Inventory VALUES (?,?,?,?,?,?)",[lib,id,input("Enter Title: "),input("Enter Genre: "),int(input("Enter Quantity: ")),0])
        conn.commit()
        cursor.execute("INSERT INTO Book VALUES (?,?,?,?)",[id,int(input("Enter ISBN: ")),input("Enter Author: "),int(input("Enter Dewey Decimal Categorization Number: "))])
        conn.commit()
      except:
        print("Item with Inventory ID already exist")
        input()
      clear()
    elif menu == 2:
      id = int(input("Enter Inventory Number: "))
      try:
        cursor.execute("INSERT INTO Inventory VALUES (?,?,?,?,?,?)",[lib,id,input("Enter Title: "),input("Enter Genre: "),int(input("Enter Quantity: ")),0])
        conn.commit()
        cursor.execute("INSERT INTO Movie VALUES (?,?,?)",[id,input("Enter ISAN: "),input("Enter Director: ")])
        conn.commit()
      except:
        print("Item with Inventory ID already exist")
        input()
      clear()
    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function removes an inventory item from the Inventory Table and the Book/Movie Table
def Rem_Inv(conn,cursor):
  flag = True
  while flag:
    menu = int(input("[1] Remove Item\n[0] Return\n"))
    clear()

    if menu == 1:
      cursor.execute("DELETE FROM Inventory WHERE Invno = ?",[int(input("Enter Inventory ID of Item being removed: "))])
      conn.commit()
      clear()
    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Funcion adds a new Employee or Member to respective table
def Add_Person(conn,cursor,lib):
  flag = True
  while flag:
    menu = int(input("[1] Add Employee\n[2] Add Member\n[0] Return\n"))
    clear()

    if menu == 1:
      try:
        F,M,L = input("Enter Employee Name: ").split()
      except:
        print("Format Name: First Mid_Initial Last")
        input()
        clear()
        continue
      try:
        cursor.execute("INSERT INTO Employee VALUES (?,?,?,?,?,?,?,?)",[lib,int(input("Enter Social Security Number: ")),int(input("Enter Employee Salary: ")),input("Enter Employee Address: "),F,M,L,input("Enter Employee Password: ")])
        conn.commit()
      except:
        print("Employee with SSN already exist")
        input()
      
      clear()
    elif menu == 2:
      try:
        F,M,L = input("Enter Member Name: ").split()
      except:
        print("Format Name: First Mid_Initial Last")
        input()
        clear()
        continue
      try:
        cursor.execute("INSERT INTO Member VALUES (?,?,?,?,?,?)",[int(input("Enter Member ID Number: ")),lib,F,M,L,input("Enter Member Address: ")])
        conn.commit()
      except:
        print("Member with Member ID already exist")
        input()
      clear()
    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function removes a person from the Employee Table or the Member Table
def Rem_Person(conn,cursor):
  flag = True
  while flag:
    menu = int(input("[1] Remove Employee\n[2] Remove Member\n[0] Return\n"))
    clear()

    if menu == 1:
      cursor.execute("DELETE FROM Employee WHERE Ssn = ?",[int(input("Enter Social Security Number of Employee being removed: "))])
      conn.commit()
      clear()
    elif menu == 2:
      cursor.execute("DELETE FROM Member WHERE LibID = ?",[int(input("Enter ID Number of Member being removed: "))])
      conn.commit()
      clear()
    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function runs Query to find books matching criteria
def Query_for_Book(cursor,lib):
  flag = True
  while flag:
    menu = int(input("[1] By Inventory Number\n[2] By Title\n[3] By Genre\n[4] By Availability\n[5] By ISBN\n[6] By Author\n[7] By Dewey Decimal Number\n[8] Display All Books\n[0] Return\n"))
    clear()

    if menu == 1:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE I.Invno = ? AND I.Libname = ? ORDER BY I.Invno ASC",[int(input("Enter Inventory ID: ")),lib])

      clear()
      Print_Table(cursor,res)
      input()
      clear()

    elif menu == 2:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE I.Title = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Title: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 3:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE I.Genre = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Genre: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 4:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE I.Quantity-I.Qborrowed > 0  AND I.Libname = ? ORDER BY I.Invno ASC",[lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 5:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE B.Isbn = ? AND I.Libname = ? ORDER BY I.Invno ASC",[int(input("Enter ISBN: ")),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 6:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE B.Author = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Author: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 7:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE B.DDCno = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Dewey Decimal Number: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 8:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,B.Isbn,B.Author,B.DDCno \"Dewey Decimal Number\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE I.Libname = ? ORDER BY I.Invno ASC",[lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function runs Query to find movies matching criteria
def Query_for_Movie(cursor,lib):
  flag = True
  while flag:
    menu = int(input("[1] By Inventory Number\n[2] By Title\n[3] By Genre\n[4] By Availability\n[5] By ISAN\n[6] By Director\n[7] Display All Movies\n[0] Return\n"))
    clear()

    if menu == 1:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE I.Invno = ? AND I.Libname = ? ORDER BY I.Invno ASC",[int(input("Enter Inventory ID: ")),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 2:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE I.Title = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Title: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 3:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE I.Genre = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Genre: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 4:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE I.Quantity-I.Qborrowed > 0 AND I.Libname = ? ORDER BY I.Invno ASC",[lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 5:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE M.Isan = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter ISAN: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 6:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE M.Director = ? AND I.Libname = ? ORDER BY I.Invno ASC",[input("Enter Director: "),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 7:
      res = cursor.execute("SELECT I.Invno \"Inventory ID\",I.Title,I.Genre,I.Quantity,I.Quantity-I.Qborrowed Availability,M.Isan,M.Director FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE I.Libname = ? ORDER BY I.Invno ASC",[lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function finds information of Members who are borrowing Inventory item
def Query_for_Borrower(cursor,lib):
  flag = True
  while flag:
    menu = int(input("[1] Borrowing\n[0] Return\n"))
    clear()

    if menu == 1:
      res = cursor.execute("SELECT M.LibID,M.Fname,M.Minitial,M.Lname FROM Member M JOIN Borrows B ON M.LibID = B.LibID WHERE B.Invno = ? AND M.Libname = ?",[int(input("Enter Inventory ID: ")),lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()
    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function finds items being borrowed by a specific Member
def Query_for_Borrowed_Items(cursor,lib,mem=None):
  flag = True
  while flag:
    menu = int(input("[1] Borrowed By\n[0] Return\n"))
    clear()

    if menu == 1:
      if mem == None:
        id = int(input("Enter Library ID: "))
      else:
        id = mem

      clear()
      res = cursor.execute("SELECT I.Invno \"Inventory Number\",I.Title,I.Genre,B.Isbn,B.Author,B.DDCno \"Dewey Decimal No.\" FROM Inventory I JOIN Borrows Bo ON I.Invno = Bo.Invno JOIN Book B ON I.Invno = B.Invno WHERE Bo.LibID = ? AND I.Libname = ?",[id,lib])
      print("Books Borrowed:")
      Print_Table(cursor,res)

      res = cursor.execute("SELECT I.Invno \"Inventory Number\",I.Title,I.Genre,M.Isan,M.Director FROM Inventory I JOIN Borrows B ON I.Invno = B.Invno JOIN Movie M ON I.Invno = M.Invno WHERE B.LibID = ? AND I.Libname = ?",[id,lib])
      print("\nMovies Borrowed:")
      Print_Table(cursor,res)    
      input()
      clear()

    elif menu == 0:
      flag = False
      clear()
    else:
      clear()

# Function add new entry to Borrows Table and modifies Inventory.QBorrowed to be +1
def Check_Out_Item(conn,cursor,lib,mem=None):
  flag = True
  while flag:
    menu = int(input("[1] Check-Out Item\n[0] Return\n"))
    clear()

    if menu == 1:
      if mem == None:
        id = int(input("Enter Member ID: "))
      else:
        id = mem
      item = int(input("Enter Inventory ID of Item: "))
      
      res = cursor.execute("SELECT Quantity,Qborrowed FROM Inventory WHERE Invno = ? AND Libname = ?",[item,lib])
      fetch = res.fetchone()
      if fetch[0] - fetch[1] > 0:
        try:
          cursor.execute("INSERT INTO Borrows VALUES (?,?)",[id,item])
          conn.commit()

          res = cursor.execute("SELECT Qborrowed FROM Inventory WHERE Invno = ? AND Libname = ?",[item,lib])
          for i in res:
            q = i[0] + 1
          cursor.execute("UPDATE Inventory SET Qborrowed = ? WHERE Invno = ? AND Libname = ?",[q,item,lib])
          conn.commit()
        except:
          print("Member already borrowing Inventory Item")
          input()
      else:
        print("Item not Available")
        input()
      clear()

    elif menu == 0:
      flag=False
      clear()
    else:
      clear()

# Function removes entry from Borrows Table and modifies Inventory.QBorrowed to be -1
def Check_In_Item(conn,cursor,lib,mem=None):
  flag = True
  while flag:
    menu = int(input("[1] Check-In Item\n[0] Return\n"))
    clear()

    if menu == 1:
      if mem == None:
        id = int(input("Enter Member ID: "))
      else:
        id = mem
      item = int(input("Enter Inventory ID of Item: "))

      if cursor.execute("SELECT * FROM Borrows WHERE LibID = ? AND Invno = ?",[id,item]).fetchone() != None:
        cursor.execute("DELETE FROM Borrows WHERE LibID = ? AND Invno = ? ",[id,item])
        conn.commit()

        res = cursor.execute("SELECT Qborrowed FROM Inventory WHERE Invno = ? AND Libname = ?",[item,lib])
        for i in res:
          q = i[0] - 1
        cursor.execute("UPDATE Inventory SET Qborrowed = ? WHERE Invno = ? AND Libname = ?",[q,item,lib])
        conn.commit()
      clear()

    elif menu == 0:
      flag=False
      clear()
    else:
      clear()

# Function compiles a table of useful aggregated data and displays it
def Generate_Report(cursor,lib):
  flag = True
  
  while flag:
    menu = int(input("[1] Generate Employee Report\n[2] Generate Member Report\n[3] Inventory Report\n[0] Return\n"))
    clear()

    if menu == 1:
      res = cursor.execute("SELECT COUNT(*)-1 \"# of Employees\",AVG(Salary) \"Avg Salary\",MAX(Salary) \"Highest Salary\",SUM(Salary) \"Total Payroll\" FROM Employee WHERE Libname = ?",[lib])

      clear()
      Print_Table(cursor,res)      
      input()
      clear()

    elif menu == 2:
      table = []
      res = cursor.execute("SELECT COUNT(*) \"# of Members\" FROM Member WHERE Libname = ?",[lib])

      print("|",end="")
      it = 0
      for i in res.description:    
        print(i[0].center(20),end='')
        print("|",end="")
        it = it + 1
      for i in res:
        for j in i:
          table.append(j)

      res = cursor.execute("SELECT COUNT(*) \"# of Items Borrowed\" FROM Borrows B JOIN Member M ON M.LibID = B.LibID WHERE Libname = ?",[lib])

      for i in res.description:    
        print(i[0].center(21),end='')
        print("|",end="")
        it = it + 1
      for i in res:
        for j in i:
          table.append(j)

      res = cursor.execute("SELECT AVG(Borrowed) \"Avg # of Items Borrowed\",MAX(Borrowed) \"Max # of Items Borrowed By Single Person\" FROM (SELECT COUNT(*) Borrowed FROM Borrows B JOIN Member M ON M.LibID = B.LibID WHERE Libname = ? GROUP BY M.LibID)",[lib])

      for i in res.description:    
        print(i[0].center(40),end='')
        print("|",end="")
        it = it + 1
      for i in res:
        for j in i:
          table.append(j)
      print()

      print("".center(126,"-"))

      print("|",end="")
      print(str(table[0]).center(20),end="")
      print("|",end="")
      print(str(table[1]).center(21),end="")
      print("|",end="")
      print(str(round(table[2])).center(40),end="")
      print("|",end="")
      print(str(table[3]).center(40),end="")
      print("|",end="")
      print()
      input()

    elif menu == 3:
      table = []
      res = cursor.execute("SELECT SUM(Quantity) \"# of Items in Inventory\",SUM(Qborrowed) \"# of Items Borrowed\" FROM Inventory WHERE Libname = ?",[lib])

      print("|",end="")
      it = 0
      for i in res.description:    
        print(i[0].center(25),end='')
        print("|",end="")
        it = it + 1
      for i in res:
        for j in i:
          table.append(j)

      res = cursor.execute("SELECT SUM(I.Quantity) \"# of Books in Inventory\",SUM(I.Qborrowed) \"# of Books Borrowed\" FROM Inventory I JOIN Book B ON I.Invno = B.Invno WHERE Libname = ?",[lib])

      for i in res.description:    
        print(i[0].center(25),end='')
        print("|",end="")
        it = it + 1
      for i in res:
        for j in i:
          table.append(j)

      res = cursor.execute("SELECT SUM(I.Quantity) \"# of Movies in Inventory\",SUM(I.Qborrowed) \"# of Movies Borrowed\" FROM Inventory I JOIN Movie M ON I.Invno = M.Invno WHERE Libname = ?",[lib])

      for i in res.description:    
        print(i[0].center(25),end='')
        print("|",end="")
        it = it + 1
      for i in res:
        for j in i:
          table.append(j)
      print()

      print("".center(it*26+1,"-"))

      print("|",end="")
      for i in table:
        print(str(i).center(25),end="")
        print("|",end="")
      print()
      input()

    elif menu == 0:
      flag = False

    clear()