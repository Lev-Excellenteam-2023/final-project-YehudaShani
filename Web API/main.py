# This program will run a HTTP server using flask and will be used to handle requests from the client
# Requests include: Uploading a file, checking the status of a file, and downloading a file

from flask import Flask, render_template, request
from datetime import datetime
import os
import uuid
import json

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = 'C:\\Users\\yehuda\\Documents\\ExcelenTeam\\Python\\Exercises\\GPT API\\content\\uploads'
app.config['OUTPUT_FOLDER'] = 'C:\\Users\\yehuda\\Documents\\ExcelenTeam\\Python\\Exercises\\GPT API\\content\\outputs'


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
        return render_template('home.html', file_id=json.dumps({"uid": file_id}))

    else:
        return 'No file uploaded.'


# Route for checking upload status
@app.route('/status', methods=['POST'])
def check_status():
    # get file id from request
    file_id = request.form['upload_id']
    # check if file exists
    for file in os.listdir(app.config['OUTPUT_FOLDER']):
        file_ending = file_id + '.json'
        if file.endswith(file_ending):
            # check if file has only '['
            with open(os.path.join(app.config['OUTPUT_FOLDER'], file), 'r') as f:
                if f.read() == '' or f.read() == '[':
                    json_answer = json.dumps({"status": "processing"})
                else:
                    json_answer = json.dumps({"status": "ready"})

    return render_template('home.html', status_answer=json_answer)


def generate_id():
    # generate json file id
    return str(uuid.uuid4())


if __name__ == '__main__':
    app.run()
