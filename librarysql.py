import sqlite3

# Connect to the database
connection = sqlite3.connect("library.db")
cursor = connection.cursor()

# Create AUTHOR table
author_table = """
CREATE TABLE AUTHOR (
    AUTHOR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(50),
    BIRTHDATE DATE,
    NATIONALITY VARCHAR(50)
)
"""
cursor.execute(author_table)

# Create BOOK table
book_table = """
CREATE TABLE BOOK (
    BOOK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE VARCHAR(100),
    AUTHOR_ID INTEGER,
    PUBLISHER VARCHAR(50),
    YEAR_PUBLISHED INT,
    GENRE VARCHAR(50),
    ISBN VARCHAR(13),
    FOREIGN KEY (AUTHOR_ID) REFERENCES AUTHOR(AUTHOR_ID)
)
"""
cursor.execute(book_table)

# Create MEMBER table
member_table = """
CREATE TABLE MEMBER (
    MEMBER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(50),
    EMAIL VARCHAR(50),
    PHONE VARCHAR(15),
    ADDRESS VARCHAR(100),
    JOIN_DATE DATE
)
"""
cursor.execute(member_table)

# Create LOAN table
loan_table = """
CREATE TABLE LOAN (
    LOAN_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BOOK_ID INTEGER,
    MEMBER_ID INTEGER,
    LOAN_DATE DATE,
    RETURN_DATE DATE,
    DUE_DATE DATE,
    STATUS VARCHAR(20),
    FOREIGN KEY (BOOK_ID) REFERENCES BOOK(BOOK_ID),
    FOREIGN KEY (MEMBER_ID) REFERENCES MEMBER(MEMBER_ID)
)
"""
cursor.execute(loan_table)

# Insert sample data into AUTHOR table
cursor.execute("INSERT INTO AUTHOR (NAME, BIRTHDATE, NATIONALITY) VALUES ('J.K. Rowling', '1965-07-31', 'British')")
cursor.execute("INSERT INTO AUTHOR (NAME, BIRTHDATE, NATIONALITY) VALUES ('George R.R. Martin', '1948-09-20', 'American')")
cursor.execute("INSERT INTO AUTHOR (NAME, BIRTHDATE, NATIONALITY) VALUES ('J.R.R. Tolkien', '1892-01-03', 'British')")
cursor.execute("INSERT INTO AUTHOR (NAME, BIRTHDATE, NATIONALITY) VALUES ('Isaac Asimov', '1920-01-02', 'American')")

# Insert sample data into BOOK table
cursor.execute("INSERT INTO BOOK (TITLE, AUTHOR_ID, PUBLISHER, YEAR_PUBLISHED, GENRE, ISBN) VALUES ('Harry Potter and the Sorcerer''s Stone', 1, 'Bloomsbury', 1997, 'Fantasy', '9780747532743')")
cursor.execute("INSERT INTO BOOK (TITLE, AUTHOR_ID, PUBLISHER, YEAR_PUBLISHED, GENRE, ISBN) VALUES ('A Game of Thrones', 2, 'Bantam Spectra', 1996, 'Fantasy', '9780553103540')")
cursor.execute("INSERT INTO BOOK (TITLE, AUTHOR_ID, PUBLISHER, YEAR_PUBLISHED, GENRE, ISBN) VALUES ('The Hobbit', 3, 'George Allen & Unwin', 1937, 'Fantasy', '9780048231887')")
cursor.execute("INSERT INTO BOOK (TITLE, AUTHOR_ID, PUBLISHER, YEAR_PUBLISHED, GENRE, ISBN) VALUES ('Foundation', 4, 'Gnome Press', 1951, 'Science Fiction', '9780586010808')")

# Insert sample data into MEMBER table
cursor.execute("INSERT INTO MEMBER (NAME, EMAIL, PHONE, ADDRESS, JOIN_DATE) VALUES ('Alice Johnson', 'alice.johnson@example.com', '555-1234', '123 Main St, Anytown, USA', '2023-01-15')")
cursor.execute("INSERT INTO MEMBER (NAME, EMAIL, PHONE, ADDRESS, JOIN_DATE) VALUES ('Bob Smith', 'bob.smith@example.com', '555-5678', '456 Oak St, Sometown, USA', '2023-03-22')")
cursor.execute("INSERT INTO MEMBER (NAME, EMAIL, PHONE, ADDRESS, JOIN_DATE) VALUES ('Carol White', 'carol.white@example.com', '555-8765', '789 Pine St, Yourtown, USA', '2023-05-10')")
cursor.execute("INSERT INTO MEMBER (NAME, EMAIL, PHONE, ADDRESS, JOIN_DATE) VALUES ('David Brown', 'david.brown@example.com', '555-4321', '321 Maple St, Heretown, USA', '2023-07-05')")

# Insert sample data into LOAN table
cursor.execute("INSERT INTO LOAN (BOOK_ID, MEMBER_ID, LOAN_DATE, RETURN_DATE, DUE_DATE, STATUS) VALUES (1, 1, '2023-07-01', '2023-07-15', '2023-07-15', 'Returned')")
cursor.execute("INSERT INTO LOAN (BOOK_ID, MEMBER_ID, LOAN_DATE, RETURN_DATE, DUE_DATE, STATUS) VALUES (2, 2, '2023-07-05', NULL, '2023-07-19', 'Overdue')")
cursor.execute("INSERT INTO LOAN (BOOK_ID, MEMBER_ID, LOAN_DATE, RETURN_DATE, DUE_DATE, STATUS) VALUES (3, 3, '2023-07-10', NULL, '2023-07-24', 'On Loan')")
cursor.execute("INSERT INTO LOAN (BOOK_ID, MEMBER_ID, LOAN_DATE, RETURN_DATE, DUE_DATE, STATUS) VALUES (4, 4, '2023-07-15', '2023-07-20', '2023-07-29', 'Returned')")

# Fetch and print data from AUTHOR table
print("AUTHOR records are:")
data = cursor.execute("SELECT * FROM AUTHOR")
for row in data:
    print(row)

# Fetch and print data from BOOK table
print("BOOK records are:")
data = cursor.execute("SELECT * FROM BOOK")
for row in data:
    print(row)

# Fetch and print data from MEMBER table
print("MEMBER records are:")
data = cursor.execute("SELECT * FROM MEMBER")
for row in data:
    print(row)

# Fetch and print data from LOAN table
print("LOAN records are:")
data = cursor.execute("SELECT * FROM LOAN")
for row in data:
    print(row)

# Always close the connection
connection.commit()
connection.close()
