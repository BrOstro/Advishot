import json
import os
import secrets
import time
from os.path import splitext
from pathlib import Path

from flask import Flask, request

from config import Config

from PIL import Image


image_extensions = ['.png', '.jpeg', '.jpg', '.gif']
vidya_extensions = ['.mp4', '.avi']

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if request.form.to_dict(flat=False)['secret_key'][0] == app.config['SECRET_KEY']:
            file = request.files['sharex']
            extension = splitext(file.filename)[1]
            file.flush()
            size = os.fstat(file.fileno()).st_size

            #if extension in image_extensions:


            if extension not in image_extensions:
                return 'File type is not supported', 415

            elif size > 6000000:
                return 'File size too large', 400

            else:
                image = Image.open(file)
                data = list(image.getdata())
                file_without_exif = Image.new(image.mode, image.size)
                file_without_exif.putdata(data)

                '''Save the image with a new randomly generated filename in the desired path, and return URL info.'''
                date_string = time.strftime("/%Y/%m/%d")
                filename = secrets.token_urlsafe(5)
                file_path = os.path.join(app.config['STORAGE_FOLDER'], date_string)

                print(file_path)
                os.makedirs(file_path)
                #Path(file_path).mkdir(parents=True, exist_ok=True, mode=0o777)

                final_path = os.path.join(file_path, filename + extension)

                file_without_exif.save(final_path)
                return json.dumps({"filename": final_path, "extension": extension}), 200


if __name__ == '__main__':
    app.run()
