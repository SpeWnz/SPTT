from flask import Flask, render_template, render_template_string, send_from_directory, abort, send_file, request, redirect, url_for
import os
import ZHOR_Modules.timestampsUtils as tsu
import ZHOR_Modules.jsonUtils as jsu

app = Flask(__name__)
CONFIG = jsu.loadConfig()

# Create the "uploads" and "downloads" folders if they don't exist
os.makedirs(CONFIG['download-folder'], exist_ok=True)
os.makedirs(CONFIG['upload-folder'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

# inspired by this
# https://stackoverflow.com/a/23724948
@app.route('/dl', defaults={'req_path': ''})
@app.route('/dl/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = CONFIG['download-folder']

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('downloads.html', files=files)


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
        file.save(os.path.join(CONFIG['upload-folder'], file.filename))
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
