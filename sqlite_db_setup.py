import sqlite3

conn = sqlite3.connect('library_database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE readers (rname TEXT, ssn TEXT, address TEXT, mail TEXT, phone TEXT)')
conn.execute('CREATE TABLE staffs (sname TEXT, empid TEXT)')
print("Table created successfully")
conn.close()