from flask import Flask, request
import logging
from datetime import datetime
from ZHOR_Modules.csvUtils import getTimeStamp

app = Flask(__name__)

logging.basicConfig(filename='log.txt',level=logging.INFO, format ='%(message)s')

def log_request():
    log_message = f'{getTimeStamp()} --- {request.remote_addr}{request.path}'
    logging.info(log_message)

@app.route('/',defaults={'path':''},methods=['GET','POST'])
@app.route('/<path:path>',methods=['GET','POST'])
def catch_all(path):
    log_request()
    return 'ok'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=False)