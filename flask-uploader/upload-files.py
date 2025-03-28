from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Create an 'uploads' folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

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

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=7654)
