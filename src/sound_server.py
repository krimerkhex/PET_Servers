from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import mimetypes
import time
from functools import wraps
from loguru import logger


def Loger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        logger.info(f"function start: ({func.__name__}) with parameters: {args} :\n")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            logger.info(f"The function ({func.__name__}) ended with the result: {result}")
            logger.info(f"The function ({func.__name__}) has been completed for {(time.perf_counter() - start):.4f}\n")
        except Exception:
            logger.exception(f"the function ({func.__name__}) ended with an error\n")
        return result

    return wrapper


app = Flask(__name__)
songs_folder = 'uploads'
allow_formats = {'mp3', 'ogg', 'wav'}
app.config['UPLOAD_FOLDER'] = songs_folder


@Loger
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allow_formats


@Loger
def get_mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


@Loger
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
        else:
            return "Non-audio file detected"
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files, get_mime_type=get_mime_type)


@app.route('/play/<filename>', methods=['GET'])
def play(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, mimetype=get_mime_type(filename))


if __name__ == '__main__':
    app.run(port=8888)
