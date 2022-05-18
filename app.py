import os
from os.path import splitext

from flask import Flask, request

from config import Config


image_extensions = ['.png', '.jpeg', '.jpg', '.gif']

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if request.form.to_dict(flat=False)['secret_key'][0] == "test": #app.config['SECRET_KEY']:
            file = request.files['sharex']
            extension = splitext(file.filename)[1]
            file.flush()
            size = os.fstat(file.fileno()).st_size
            if extension not in image_extensions:
                return 'File type is not supported', 415

            elif size > 6000000:
                return 'File size too large', 400

            else:
                return extension


if __name__ == '__main__':
    app.run()
