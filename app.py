from flask import Flask, request, redirect, render_template, Response
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

#app.secret_key = os.environ.get('SECRET_KEY')
#app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

app.secret_key = "SECRETKEYFORGUTECIMAGE"
app.config['UPLOAD_FOLDER'] = "static/upload"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    filepath = "no"
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        print("File: "+file.filename)

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return render_template("index.html", filename=filepath)

    return render_template("index.html", filename=filepath)


if __name__ == '__main__':
    app.run()
