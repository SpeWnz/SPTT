from flask import Flask, render_template, request, redirect, url_for
import os
import ZHOR_Modules.timestampsUtils as tsu

app = Flask(__name__)

# Create an 'uploads' folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

# upload via gui
@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    # If the user doesn't select a file or selects a file with no name
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Save the file to the 'uploads' folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return f"File uploaded successfully: {file.filename}"

    return "Invalid file format. Please try again."

# upload via curl post
# curl -X POST --data-binary "@filename.txt" http://127.0.0.1:7654/curl
@app.route('/curl', methods=['POST'])
def receive_file():
    file_data = request.get_data()  # or request.data

    file_name = None
    if 'File-Name' in request.headers:
        file_name = request.headers['File-Name']
    else:
        file_name = tsu.getTimeStamp_iso8601()

    with open(f'uploads/{file_name}', 'wb') as f:
        f.write(file_data)

    return 'File received successfully', 200
        
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=7654)
