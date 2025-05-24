import sqlite3

DATABASE = None

# create tables if they do not exist
def initializeTables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

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

    # interesting files table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interesting_files (
            file_path TEXT,
            category TEXT,
            extension TEXT
        );
    """)

    conn.commit()
    conn.close()


# takes the two large in-memory lists of matches and stores them in to the database
def insertMatches(wordlistMatches: list, regexMatches: list):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    wordlistMatches_query = "INSERT INTO wordlist_matches (file_path, extension, word) VALUES "
    for _item in wordlistMatches:
            for _subitem in _item[-1]:
                wordlistMatches_query += f'("{_item[0]}","{_item[1]}","{_subitem}"),'

    cursor.execute(wordlistMatches_query[:-1])

    regexMatches_query = "INSERT INTO regex_matches (file_path, extension, regex, value) VALUES "
    for _item in regexMatches:
            for _subitem in _item[-1]:                
                # encode to hex to avoid sqlite bullshittery
                _hexValue = str(_subitem[1]).encode("utf-8").hex()
                regexMatches_query += f'("{_item[0]}","{_item[1]}","{_subitem[0]}",X\'{_hexValue}\'),'
    
    cursor.execute(regexMatches_query[:-1])
    conn.commit()
    conn.close()


def insert_interestingFile(file_path: str, category: str, extension: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
            INSERT INTO interesting_files (file_path, category, extension)
            VALUES (?, ?, ?)
        """, (file_path, category, extension))

    conn.commit()
    conn.close()