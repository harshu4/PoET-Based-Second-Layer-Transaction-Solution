import sqlite3
conn = sqlite3.connect('aadhar2.db')
conn.execute('''CREATE TABLE new_employee
         (id INT PRIMARY KEY     NOT NULL,
         name           TEXT    NOT NULL,
         photo  BLOB     NOT NULL,

         resume       TEXT NOT NULL);''')
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(empId, name, photo, resumeFile):
    try:
        sqliteConnection = sqlite3.connect('aadhar2.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO 'new_employee'
                                  ('id', 'name', 'photo', 'resume') VALUES (?, ?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        resume = resumeFile
        # Convert data into tuple format
        data_tuple = (empId, name, empPhoto, resume)
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

insertBLOB(1, "Smith", "/home/boredalchemist/Downloads/fig.bmp", "sdfsdf")
