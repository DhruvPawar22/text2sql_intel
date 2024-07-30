import sqlite3

connection=sqlite3.connect("student.db")


cursor=connection.cursor()


table_info="""
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""


cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Dhruv','Data Science','A',60)''')
cursor.execute('''Insert Into STUDENT values('Ashwin','Artificial Intelligence','A',80)''')
cursor.execute('''Insert Into STUDENT values('Yatin','Cyber Security','A',90)''')


print("inserted records are")
data=cursor.execute('''Select * From Student''')

for row in data:
    print(row)
    
    
#always close connection

connection.commit()
connection.close()