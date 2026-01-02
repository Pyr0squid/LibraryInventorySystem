-- tested with SQLite

CREATE TABLE Library(
  Name Str PRIMARY KEY,
  LibAdd Str,
  Phone Int(10)
);

CREATE TABLE Employee(
  Libname Str REFERENCES Library(Name)
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  Ssn Int(9) PRIMARY KEY,
  Salary Int,
  EmpAdd Str,
  Fname Str,
  Minitial Char(1),
  Lname Str,
  Password Str
);

CREATE TABLE Member(
  LibID Int PRIMARY KEY,
  Libname Str REFERENCES Library(Name)
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  Fname Str,
  Minitial Char(1),
  Lname Str,
  MemAdd Str
);

CREATE TABLE Inventory(
  Libname Str REFERENCES Library(Name)
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  Invno Int PRIMARY KEY,
  Title Str,
  Genre Str,
  Quantity Int,
  Qborrowed Int
);

CREATE TABLE Book(
  Invno Int REFERENCES Inventory
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  Isbn Int PRIMARY KEY,
  Author Str,
  DDCno Int
);

CREATE TABLE Movie(
  Invno Int REFERENCES Inventory
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  Isan Str PRIMARY KEY,
  Director Str
);

CREATE TABLE Borrows(
  LibID Int REFERENCES Member
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  Invno Int REFERENCES Inventory
    ON DELETE CASCADE  
    ON UPDATE CASCADE,
  PRIMARY KEY(LibID,Invno)
);

INSERT INTO Library
  VALUES('Rolla Public Library','900 N Pine St, Rolla, MO 65401',5733642604);

INSERT INTO Employee(Libname,Ssn,Fname,Lname,Password)
  VALUES('Rolla Public Library',0,'add','min','admin');

INSERT INTO Employee
  VALUES('Rolla Public Library',1,35000,'520 Bender St, Rolla, MO 65401','Kelly','S','Velte','password1');

INSERT INTO Employee
  VALUES('Rolla Public Library',2,42000,'117 Foxfield Ln, Rolla, MO 65401','Felix','E','Line','CatzRule');

INSERT INTO Member
  VALUES(1,'Rolla Public Library','Luna','E','Lovegood','360 Trent Rd, Rolla, MO 65401');

INSERT INTO Member
  VALUES(2,'Rolla Public Library','Richard','R','Grayson','663 Gotham St, Rolla, MO 65401');

INSERT INTO Member
  VALUES(3,'Rolla Public Library','Garfield','M','Lasagna','734 Jon St, Rolla, MO 65401');

INSERT INTO Member
  VALUES(4,'Rolla Public Library','Jim','D','Butcher','250 Wizard Ln, Rolla, MO 65401');

INSERT INTO Member
  VALUES(5,'Rolla Public Library','Sally','A','Belle','882 Dumbo St, Rolla, MO 65401');

INSERT INTO Inventory
  VALUES('Rolla Public Library',1,'Magician','Fantasy',2,2);

INSERT INTO Book
  VALUES(1,9780246122056,'Raymond E. Feist',823);

INSERT INTO Inventory
  VALUES('Rolla Public Library',2,'A Darkness At Sethanon','Fantasy',1,0);

INSERT INTO Book
  VALUES(2,9780385192156,'Raymond E. Feist',823);

INSERT INTO Inventory
  VALUES('Rolla Public Library',3,'Physics for Dummies','Non-Fiction',5,1);

INSERT INTO Book
  VALUES(3,9780470219508,'Steven Holzner',530);

INSERT INTO Inventory
  VALUES('Rolla Public Library',4,'Geography for Dummies','Non-Fiction',3,1);

INSERT INTO Book
  VALUES(4,9780764516221,'Charles A. Heatwole',910);

INSERT INTO Inventory
  VALUES('Rolla Public Library',5,'Deadpool','Action',1,1);

INSERT INTO Movie
  VALUES(5,'0000-0004-257F','Tim Miller');

INSERT INTO Inventory
  VALUES('Rolla Public Library',6,'Star Wars','Science Fiction',4,1);

INSERT INTO Movie
  VALUES(6,'0000-0000-EB93','George Lucas');

INSERT INTO Inventory
  VALUES('Rolla Public Library',7,'The Crocodile Hunter','Documentary',2,1);

INSERT INTO Movie
  VALUES(7,'0000-0002-8D02','John Stainton');

INSERT INTO Borrows
  VALUES(1,7);

INSERT INTO Borrows
  VALUES(1,1);

INSERT INTO Borrows
  VALUES(2,3);

INSERT INTO Borrows
  VALUES(4,1);

INSERT INTO Borrows
  VALUES(4,4);

INSERT INTO Borrows
  VALUES(4,5);

INSERT INTO Borrows
  VALUES(4,6);