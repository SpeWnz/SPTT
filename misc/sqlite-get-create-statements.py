import sqlite3
import sys
import os

def print_create_table_statements(db_path):
    if not os.path.exists(db_path):
        print(f"Error: File '{db_path}' does not exist.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch all CREATE TABLE statements from sqlite_master
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL;")
        create_statements = cursor.fetchall()

        if not create_statements:
            print("No CREATE TABLE statements found.")
        else:
            for stmt in create_statements:
                print(stmt[0])
                print()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_sqlite_db>")
    else:
        db_path = sys.argv[1]
        print_create_table_statements(db_path)
