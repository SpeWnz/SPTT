import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.logUtils as logu
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.timestampsUtils as tsu

import threading
import time
import sys

# mysql
import mysql.connector

# mongo db
import pymongo

# postgresql
import psycopg2

# mysql
import mysql

# mssql
import pyodbc

# ibm db2
import ibm_db

_VERSION = "v300525"
CONNECTION_TIMEOUT = 1          # seconds
LOG_LOCK = threading.Lock()
STDOUT_LOCK = threading.Lock()
LOG_PATH = f"logs/log_{tsu.getTimeStamp_iso8601()}.log"
SUPPORTED_DBMSES = ['mongodb','mysql','postgresql','mssql','ibmdb2'] #mongodb, mysql, postgresql, mssql

# dbms specific flags
MYSQL_DISABLE_SSL       = False
IBMDB2_DATABASE         = 'sampledb'

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
    global MYSQL_DISABLE_SSL

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
            password=password,
            ssl_disabled=MYSQL_DISABLE_SSL
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

# return true, none         ----> auth ok
# return false, false       ----> auth ko or other exception (depends on returned code)
# return false, exception   ----> other exception
def connect_IBMDB2(target: str, username: str, password: str):
    global CONNECTION_TIMEOUT
    global IBMDB2_DATABASE

    values = target.split(':')
    server = values[0]
    port = values[1]

    # Create the connection string without a database
    connection_string = f'DRIVER={{DB2}};DATABASE={IBMDB2_DATABASE};HOSTNAME={server};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};'
    #np.debugPrint(connection_string)

    # Establish the connection
    try:
        conn = ibm_db.connect(connection_string, '', '')
        ibm_db.close(conn)

        # auth ok
        return True,None

    # exception
    except Exception as e:
        
        # auth ko
        if '[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082' in str(e):
            return False, False

        # other exceptions        
        return False, e

# return true, none         ----> auth ok
# return false, false       ----> auth ko or other exception (depends on returned code)
# return false, exception   ----> other exception
def enum_IBMDB2_database(target: str, database: str):
    global CONNECTION_TIMEOUT

    values = target.split(':')
    server = values[0]
    port = values[1]

    # Create the connection string without a database
    connection_string = f'DRIVER={{DB2}};DATABASE={database};HOSTNAME={server};PORT={port};PROTOCOL=TCPIP;UID=thisUsernameDoesNotExist;PWD=thisPasswordIsInvalid;'
    #np.debugPrint(connection_string)

    # Establish the connection
    try:
        conn = ibm_db.connect(connection_string, '', '')
        ibm_db.close(conn)

    # exception
    except Exception as e:
        
        # wrong credentials: database exists
        if '[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082' in str(e):
            msg = "[SUCCESS] Target {} --- Database name: {}".format(target,database)
            logu.logInfo(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            return 1

        # specific error: database does not exist
        if '[IBM][CLI Driver] SQL1001N' in str(e) and 'is not a valid database name.  SQLSTATE=2E000 SQLCODE=-1001' in str(e):
            msg = "[FAILED] Target {} --- Database name: {}".format(target,database)
            logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            return 0
        

        if '[IBM][CLI Driver] SQL30061N  The database alias or database name' in str(e) and 'was not found at the remote node.  SQLSTATE=08004 SQLCODE=-30061' in str(e):
            msg = "[FAILED] Target {} --- Database name: {}".format(target,database)
            logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            return 0

        # other types of exception
        msg = "[EXCEPTION] Target {} --- Database name: {} --- Exception: {}".format(target,database,str(e))   
        logu.logError(msg,fileName=LOG_PATH, lock=LOG_LOCK,stdout=False)  
        return -1

# return true, none         ----> auth ok
# return false, false       ----> auth ko or other exception (depends on returned code)
# return false, exception   ----> other exception
def enum_IBMDB2_username(target: str, database: str):
    global CONNECTION_TIMEOUT

    values = target.split(':')
    server = values[0]
    port = values[1]

    # Create the connection string without a database
    connection_string = f'DRIVER={{DB2}};DATABASE={database};HOSTNAME={server};PORT={port};PROTOCOL=TCPIP;UID=thisUsernameDoesNotExist;PWD=thisPasswordIsInvalid;'
    #np.debugPrint(connection_string)

    # Establish the connection
    try:
        conn = ibm_db.connect(connection_string, '', '')
        ibm_db.close(conn)

    # exception
    except Exception as e:
        
        # wrong credentials: database exists
        if '[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082' in str(e):
            msg = "[SUCCESS] Target {} --- Database name: {}".format(target,database)
            logu.logInfo(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            return 1

        # specific error: database does not exist
        if '[IBM][CLI Driver] SQL1001N' in str(e) and 'is not a valid database name.  SQLSTATE=2E000 SQLCODE=-1001' in str(e):
            msg = "[FAILED] Target {} --- Database name: {}".format(target,database)
            logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            return 0
        

        if '[IBM][CLI Driver] SQL30061N  The database alias or database name' in str(e) and 'was not found at the remote node.  SQLSTATE=08004 SQLCODE=-30061' in str(e):
            msg = "[FAILED] Target {} --- Database name: {}".format(target,database)
            logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            return 0

        # other types of exception
        msg = "[EXCEPTION] Target {} --- Database name: {} --- Exception: {}".format(target,database,str(e))   
        logu.logError(msg,fileName=LOG_PATH, lock=LOG_LOCK,stdout=False)  
        return -1



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

    if database == 'ibmdb2':
        result, exception = connect_IBMDB2(target,username,password)

    # auth ok
    if result == True:
        msg = "[SUCCESS] [{}] Target {} --- User: {} --- Password: {}".format(database,target,username,password)
        logu.logInfo(msg,fileName=LOG_PATH,lock=LOG_LOCK)
        return 1

    # auth ko
    if result == False and exception == False:
        msg = "[FAILED] [{}] Target {} --- User: {} --- Password: {}".format(database,target,username,password)
        logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
        return 0

    # exception
    if result == False:
        msg_stdout = "[EXCEPTION] [{}] Target {} --- User: {} --- Password: {} --- check log for details".format(database,target,username,password)
        msg_log = "[EXCEPTION] [{}] Target {} --- User: {} --- Password: {} --- {}".format(database,target,username,password,str(exception))
        np.errorPrint(msg_stdout,lock=STDOUT_LOCK)        
        logu.logError(msg_log,fileName=LOG_PATH, lock=LOG_LOCK,stdout=False)   
        return -1
