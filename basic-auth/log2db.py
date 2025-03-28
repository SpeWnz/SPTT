import sqlite3
import ZHOR_Modules.fileManager as fm
import sys

def writeCache(db, target, user, password, result):
  
    # Connect to the SQLite database (it will create the database if it does not exist)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    _tuple = (target, user, password, result)
    #print(_tuple)

    # Insert the values into the table
    cursor.execute('''
    INSERT INTO cached_results (target, user, password, result)
    VALUES (?, ?, ?, ?)
    ''', _tuple)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


def dbCheck(db):
    
    # Connect to the SQLite database (it will create the database if it does not exist)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cached_results (
        target TEXT,
        user TEXT,
        password TEXT,
        result TEXT
    )
    ''')

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


lines = fm.fileToSimpleList(str(sys.argv[1]))
db = str(sys.argv[2])
dbCheck(db)

for l in lines:
    # [ERROR] [EXCEPTION] Target 127.0.0.1:8000 | User: root | Password: password3 | HTTPSConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: / (Caused by SSLError(SSLError(1, '[SSL: RECORD_LAYER_FAILURE] record layer failure (_ssl.c:1001)')))
    
    values = l.split('|')
    #sprint(values)
    target = values[0].split(' ')[-2]
    user = values[1].split(' ')[-2]
    passw = values[2].split(' ')[-2]
    
    print(target,user,passw)

    if ('[EXCEPTION]') in l:
        writeCache(db,target,user,passw,'EXCEPTION')

    if ('[SUCCESS]') in l:
        writeCache(db,target,user,passw,'SUCCESS')            

    if ('[FAILED]') in l:
        writeCache(db,target,user,passw,'FAILED')
