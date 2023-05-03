import sqlite3
import csv

with open('./books.csv', newline='', encoding="utf-8") as f:
    csv_reader = csv.DictReader(f) 
    books = [
        (row['ISBN'], row['書名'], row['作者'], row['分類'], row['版次'])
        for row in csv_reader
        ]

with open('create_db.sql', encoding="utf-8") as f:  
    create_db_sql = f.read()

db = sqlite3.connect('books.db')
with db:
    db.executescript(create_db_sql)
    db.executemany(
        'INSERT INTO  books(ISBN, title, author, category, version) VALUES (?, ?, ?, ?, ?)',
        books
    )

db = sqlite3.connect('readers.db')
with db:
    db.executescript(create_db_sql)
    data = ('dylan','b122456731','台北市文山區','xxx@gmail.com','0935641297','5897')
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO readers(rname, ssn, address, mail, phone, password) VALUES (?, ?, ?, ?, ?, ?)',
        data
    )

db = sqlite3.connect('staffs.db')
with db:
    db.executescript(create_db_sql)
    data2 = ('dylan','b122456731')
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO staffs(sname, empid) VALUES (?, ?)',
        data2
    )