'''
"fetch companion"
a simple api server used to receive get/post requests from fetch functions within the browser console
very useful in situations like the following:
- when google dorking for files, webdrivers will get blocked. Hence, post all the href links to fetch companion
- when web scraping, printing the required information to the console needs further text filtering. By using fetch companion, you dont.

'''

from flask import Flask, jsonify, send_file, request, make_response,render_template
from flask_cors import CORS

import ZHOR_Modules.fileManager as fm

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# used for dorkFiles.js
@app.route('/dorkFiles', methods=['POST'])
def dorkFiles():
    data = request.get_json()
    
    fm.listToFile(data['data'],"dorkfiles.txt",'a')    
    
    return "OK"

# method used by clients to submit their performance
@app.route('/endpoint', methods=['POST'])
def endpoint():
    return "OK!"





# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)
