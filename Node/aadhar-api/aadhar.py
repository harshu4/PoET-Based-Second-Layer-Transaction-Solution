#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('aadhar.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE PERSON
         (AADHARNO INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         IMAGE         BLOB NOT NULL);''')
print("Table created successfully")


def insertBLOB(aadhar, name, age, address,image):
    try:
        sqliteConnection = sqlite3.connect('aadhar.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO 'PERSON'
                                  ('AADHARNO', 'NAME', 'AGE', 'ADDRESS','IMAGE') VALUES (?, ?, ?, ?,?)"""


        imagep = image

        data_tuple = (aadhar,name,age,address,imagep)
        cursor.execute(sqlite_insert_blob_query, data_tuple)

        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")



file = open("/home/boredalchemist/Downloads/fig.bmp",'rb')
image = file.read()
insertBLOB(1,'harsh',24,'dsfjfsf',image)
