import sqlite3

connection=sqlite3.connect("test.db")


cursor=connection.cursor()


table_info="""
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT, ROLLNO INT, CITY VARCHAR(25))
"""


cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Ayush','Data Science','A',90,1,'Mumbai')''')
cursor.execute('''Insert Into STUDENT values('Manish','Data Science','A',60,2,'Hyderabad')''')
cursor.execute('''Insert Into STUDENT values('Saksham','Artificial Intelligence','A',80,3,'Mumbai')''')
cursor.execute('''Insert Into STUDENT values('Mukherjee','Cyber Security','A',90,4,'Chennai')''')


print("inserted records are")
data=cursor.execute('''Select * From Student''')

for row in data:
    print(row)
    
    
#always close connection

connection.commit()
connection.close()