import threading
import ZHOR_Modules.logUtils as logu
import ZHOR_Modules.timestampsUtils as tsu

STDOUT_LOCK             = threading.Lock()
IO_LOCK                 = threading.Lock()
DATAFRAME_LOCK          = threading.Lock()
GLOBAL_MATCHES_LOCK     = threading.Lock()
LOG_PATH                = "logs/log_{}.log".format(tsu.getTimeStamp_iso8601())



def threadMessage_debug(threadID: int, message: str):
    
    msg = "[THREAD #{}] {}".format(str(threadID),message)
    logu.logDebug(message=msg,lock=STDOUT_LOCK,fileName=LOG_PATH)

def threadMessage_info(threadID: int, message: str):
    
    msg = "[THREAD #{}] {}".format(str(threadID),message)
    logu.logInfo(message=msg,lock=STDOUT_LOCK,fileName=LOG_PATH)

def threadMessage_error(threadID: int, message: str):
    
    msg = "[THREAD #{}] {}".format(str(threadID),message)
    logu.logError(message=msg,lock=STDOUT_LOCK,fileName=LOG_PATH)