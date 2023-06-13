# This program will run a HTTP server using flask and will be used to handle requests from the client
# Requests include: Uploading a file, checking the status of a file, and downloading a file

from flask import Flask, render_template, request, abort
from datetime import datetime
import os
import uuid
import json

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = 'C:\\Users\\yehuda\\Documents\\ExcelenTeam\\Python\\Exercises\\GPT API\\content\\uploads'
app.config['OUTPUT_FOLDER'] = 'C:\\Users\\yehuda\\Documents\\ExcelenTeam\\Python\\Exercises\\GPT API\\content\\outputs'


# Route for the new page
@app.route('/')
def new():
    return render_template('new.html')


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
        return render_template('new.html', file_id=json.dumps({"uid": file_id}))

    else:
        return 'No file uploaded.'


# Route for checking upload status
@app.route('/status', methods=['GET'])
def check_status():
    # get file id from request
    file_id = request.args.get('upload_id')
    # check if file exists

    for file in os.listdir(app.config['OUTPUT_FOLDER']):
        file_ending = file_id + '.json'
        if not file.endswith(file_ending):
            continue
        try:
            with open(os.path.join(app.config['OUTPUT_FOLDER'], file), 'r') as f:
                if f.read() == '[':
                    json_answer = json.dumps({"status": "processing"})
                else:
                    json_answer = json.dumps({"status": "ready"})
                    return render_template('new.html', status_answer=json_answer)

                new_json_answer = json.loads(json_answer)
                new_json_answer['timestamp'] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        except FileNotFoundError:
            abort(404)

    #add timestamp to json
    new_json_answer = json.loads(json_answer)
    new_json_answer['timestamp'] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



    return render_template('new.html', status_answer=json_answer)


def generate_id():
    # generate json file id
    return str(uuid.uuid4())


if __name__ == '__main__':
    app.run()
