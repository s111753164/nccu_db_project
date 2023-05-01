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

db = sqlite3.connect('members.db')
with db:
    db.executescript(create_db_sql)
    db.executemany(
        'INSERT INTO  members (name, group_name) VALUES (?, ?)',
        members
    )
