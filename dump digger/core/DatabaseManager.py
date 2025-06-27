import os
import sqlite3
import ZHOR_Modules.jsonUtils as jsu

DATABASE = None

# create tables if they do not exist
def initializeTables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            file_path TEXT UNIQUE, 
            category TEXT,
            extension TEXT 
        );
    """)

    # wordlist matches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wordlist_matches (
            file_path TEXT,
            extension TEXT,
            word TEXT
        );
    """)

    # regex matches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regex_matches (
            file_path TEXT,
            extension TEXT,
            regex TEXT,
            value BLOB
        );
    """)

    conn.commit()
    conn.close()


# takes the two large in-memory lists of matches and stores them in to the database
def insertMatches(wordlistMatches: list, regexMatches: list):
    
    e1 = None
    e2 = None
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # wordlist matches insertion
    if len(wordlistMatches) > 0:
        wordlistMatches_query = "INSERT INTO wordlist_matches (file_path, extension, word) VALUES "
        for _item in wordlistMatches:
                for _subitem in _item[-1]:
                    wordlistMatches_query += f'("{_item[0]}","{_item[1]}","{_subitem}"),'
        
        # for some odd reason, sometimes a query without values gets executed causing an exception.
        # as a workaround, use try-except statements and also check for the exact length of the query.
        # if it is exactly 65 then something is wrong
        if len(wordlistMatches_query) > 65:
            try:
                cursor.execute(wordlistMatches_query[:-1])
            except sqlite3.OperationalError as e:
                e1 = wordlistMatches_query[:-1]

    # regex matches insertion
    if len(regexMatches) > 0:
        regexMatches_query = "INSERT INTO regex_matches (file_path, extension, regex, value) VALUES "
        for _item in regexMatches:
                for _subitem in _item[-1]:                
                    # encode to hex to avoid sqlite bullshittery
                    _hexValue = str(_subitem[1]).encode("utf-8").hex()
                    regexMatches_query += f'("{_item[0]}","{_item[1]}","{_subitem[0]}",X\'{_hexValue}\'),'
        
        # for some odd reason, sometimes a query without values gets executed causing an exception.
        # as a workaround, use try-except statements and also check for the exact length of the query.
        # if it is exactly 65 then something is wrong
        if len(regexMatches_query) > 70:
            try:
                cursor.execute(regexMatches_query[:-1])
            except sqlite3.OperationalError as e:
                e2 = regexMatches_query[:-1]
    
    conn.commit()
    conn.close()

    return e1,e2


# inserts all the file paths and categorizes them
def makeInventory(fileList: list):

    categories = jsu.loadConfig(fileName="core/categories.json")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    for f in fileList:
        _foundCategory = ""
        _, extension = os.path.splitext(f)

        # do we have a known and interesting category?
        for cat in categories:
            if extension[1:] in categories[cat]:
                # found the category
                _foundCategory = cat
                break

            
        
        sql = f'INSERT INTO inventory VALUES (?,?,?)'
        try:
            cursor.execute(sql,(f,_foundCategory,extension,))
        
        # catch the exception regarding the "unique" constraint
        except sqlite3.IntegrityError as e:
             pass
            
            
    conn.commit()
    conn.close()