'''
"fetch companion"
a simple api server used to receive get/post requests from fetch functions within the browser console
very useful in situations like the following:
- when google dorking for files, webdrivers will get blocked. Hence, post all the href links to fetch companion
- when web scraping, printing the required information to the console needs further text filtering. By using fetch companion, you dont.

'''

from flask import Flask, jsonify, send_file, request, make_response,render_template
from flask_cors import CORS, cross_origin
import pandas
import json
from bs4 import BeautifulSoup

import ZHOR_Modules.fileManager as fm

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# used for dorkFiles.js
@app.route('/dorkFiles', methods=['POST'])
def dorkFiles():
    data = request.get_json()
    
    fm.listToFile(data['data'],"dorkfiles.txt",'a')    
    
    return "OK"

# used for dorkFiles.js
@app.route('/dorkHREFs', methods=['POST'])
def dorkHREFs():
    data = request.get_json()
    
    fm.listToFile(data['data'],"dorkHREFs.txt",'a')    
    
    return "OK"


'''
var script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'http://127.0.0.1:8081/script';
document.head.appendChild(script);
'''

@app.route('/script', methods=['GET'])
def getScript():
    return send_file('fetch-companion.js',as_attachment=True)


# method used by clients to submit their performance
@app.route('/endpoint', methods=['POST'])
def endpoint():
    return "OK!"






# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8081)
