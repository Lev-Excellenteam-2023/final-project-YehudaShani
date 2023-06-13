# This program will run a HTTP server using flask and will be used to handle requests from the client
# Requests include: Uploading a file, checking the status of a file, and downloading a file

from flask import Flask, render_template, request
from datetime import datetime
import os
import uuid

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = 'C:\\Users\\yehuda\\Documents\\ExcelenTeam\\Python\\Exercises\\GPT API\\content\\uploads'

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for handling file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_name_without_extension = os.path.splitext(file.filename)[0]
        file_name_extension = os.path.splitext(file.filename)[1]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_id = generate_id()
        filename_to_save = '-'.join([file_name_without_extension, timestamp, file_id]) + file_name_extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_to_save))
        return render_template('home.html', file_id=file_id)

    else:
        return 'No file uploaded.'

# Route for checking upload status
@app.route('/status', methods=['POST'])
def check_status():
    # Handle the upload status check logic
    # ...
    pass

def generate_id():
    # generate id using uuid
    return str(uuid.uuid4())


if __name__ == '__main__':
    app.run()