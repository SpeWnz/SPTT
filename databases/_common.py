import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.logUtils as logu
import ZHOR_Modules.listUtils as lu
from ZHOR_Modules.csvUtils import getTimeStamp

import threading
import time
import sys

# mongo db
import mysql.connector
import pymongo

# postgresql
import psycopg2

# mysql
import mysql

# mssql
import pyodbc

_VERSION = "v121024"
CONNECTION_TIMEOUT = 1          # seconds
LOG_LOCK = threading.Lock()
STDOUT_LOCK = threading.Lock()
LOG_PATH = f"log_{getTimeStamp()}.log"
SUPPORTED_DBMSES = ['mongodb','mysql','postgresql','mssql'] #mongodb, mysql, postgresql, mssql

# return true, none         ----> auth ok
# return false, false       ----> auth ko
# return false, exception   ----> other exception
def connect_MongoDB(target: str, username: str, password: str):
    global CONNECTION_TIMEOUT

    values = target.split(':')
    
    try:        
        with pymongo.timeout(CONNECTION_TIMEOUT):
            client = pymongo.MongoClient(
                host=values[0],port=int(values[1]),username=username,password=password
                )            
            client.server_info()
            return True, None

    # auth failed
    except pymongo.errors.OperationFailure as e0:
        return False, False

    # other exceptions
    except Exception as e2:
        return False, e2 

# return true, none         ----> auth ok
# return false, false       ----> auth ko
# return false, exception   ----> other exception
def connect_PostgreSQL(target: str, username: str, password: str):
    
    values = target.split(':')
    
    db_config = {
        'dbname': 'postgres',  # Connect to the default 'postgres' database
        'user': username,
        'password': password,
        'host': values[0],
        'port': values[1],
    }

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # perform sample query
        cursor.execute("SELECT datname FROM pg_database;")
        _ = cursor.fetchall()
        
        # Closing the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        return True, None

    # auth failed
    except psycopg2.OperationalError as e0:
        return False, False

    # other exceptions
    except Exception as e1:
        return False, e1


# return true, none         ----> auth ok
# return false, false       ----> auth ko or other exception (depends on returned code)
# return false, exception   ----> other exception
def connect_MySQL(target: str, username: str, password: str):
    '''
    import mysql.connector
    from mysql.connector import Error,errors
    mysql.connector.Error.AuthenticationError
    '''

    #from mysql.connector import Error,errors

    values = target.split(':')

    try:
        connection = mysql.connector.connect(
            host=values[0],
            port=values[1],
            user=username,
            password=password
        )

        # auth ok
        if connection.is_connected():
            connection.close()    
            return True, None   

    # auth ko or other exception
    except mysql.connector.Error as e0:
        if e0.errno == 1045:
            return False, False
        else:
            return False, e0
        
    
    # other exception
    except Exception as e1:
        return False, e1


# return true, none         ----> auth ok
# return false, false       ----> auth ko or other exception (depends on returned code)
# return false, exception   ----> other exception
def connect_MSSQL(target: str, username: str, password: str):
    global CONNECTION_TIMEOUT

    values = target.split(':')
    server = values[0]
    port = values[1]

    # Create the connection string without a database
    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server},{port};UID={username};PWD={password};TrustServerCertificate=yes'
    #np.debugPrint(connection_string)

    # Establish the connection
    try:
        connection = pyodbc.connect(connection_string,timeout=int(CONNECTION_TIMEOUT))
        #print("Connection successful!")
        connection.close()

        # auth ok
        return True,None


    # auth ko or other exception
    # Error in connection: ('28000', "[28000] [Microsoft][ODBC Driver 18 for SQL Server][SQL Server]Login failed for user 'your_username'. (18456) (SQLDriverConnect)")
    except pyodbc.Error as e0:
        if '28000' in str(e0):          # auth ko
            return False, False
        else:
            return False, e0
        
    # other exception
    except Exception as e1:
        return False, e1




def attemptConnection(target: str, username: str, password: str,database: str):
    result = None
    exception = None

    
    # dbms choice handling
    if database == 'mongodb':
        result, exception = connect_MongoDB(target,username,password)

    if database == 'mysql':
        result, exception = connect_MySQL(target,username,password)

    if database == 'postgresql':
        result, exception = connect_PostgreSQL(target,username,password)


    if database == 'mssql':
        result, exception = connect_MSSQL(target,username,password)
    

    # auth ok
    if result == True:
        msg = "[SUCCESS] [{}] Target {} --- User: {} --- Password: {}".format(database,target,username,password)
        logu.logInfo(msg,fileName=LOG_PATH,lock=LOG_LOCK)
        return

    # auth ko
    if result == False and exception == False:
        msg = "[FAILED] [{}] Target {} --- User: {} --- Password: {}".format(database,target,username,password)
        logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
        return

    # exception
    if result == False:
        msg_stdout = "[EXCEPTION] [{}] Target {} --- User: {} --- Password: {} --- check log for details".format(database,target,username,password)
        msg_log = "[EXCEPTION] [{}] Target {} --- User: {} --- Password: {} --- {}".format(database,target,username,password,str(exception))
        np.errorPrint(msg_stdout,lock=STDOUT_LOCK)        
        logu.logError(msg_log,fileName=LOG_PATH, lock=LOG_LOCK,stdout=False)   
        return
