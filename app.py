from flask import Flask, request, redirect, render_template
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy
import sys

numpy.set_printoptions(threshold=sys.maxsize)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

#app.secret_key = os.environ.get('SECRET_KEY')
#app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
#app.config['GIF_FOLDER'] = os.environ.get('GIF_FOLDER')

app.secret_key = "SECRETKEYFORGUTECIMAGE"
app.config['UPLOAD_FOLDER'] = "static/upload"
app.config['GIF_FOLDER'] = "static/GIF_FOLDER/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_gif(directory):

    files = os.listdir(directory)
    array = []

    for file in files:
        if "gif" in file:
            print("Gif file :"+file)
        else:
            img1 = Image.open(directory+file)
            array.append(img1)
            print("Image File: "+file)

    gif = Image.new('RGB', (400, 600))

    gif.save(directory+'out.gif', save_all=True, append_images=array, loop=0)

    return directory+'out.gif'


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    filepath = "no"
    gif = "no"
    if request.method == 'POST':
        if 'file' not in request.files or 'file2' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        file2 = request.files['file2']
        print("File: "+file.filename)
        print("File2: "+file2.filename)

        if file.filename == '' or file2.filename == '':
            return redirect(request.url)

        if (file and allowed_file(file.filename)) and (file2 and allowed_file(file2.filename)):

            filename = secure_filename(file.filename)
            filename2 = secure_filename(file2.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            file.save(filepath)
            file2.save(filepath2)

            im = Image.open(filepath)
            imgblack = im.convert('1')
            np_im = numpy.array(imgblack)
            im.close()
            # print(np_im)

            file1 = open("array.txt", "a")
            file1.write(str(np_im))
            file1.close()

            im2 = Image.open(filepath2)
            imgblack2 = im2.convert('1')
            np_im2 = numpy.array(imgblack2)
            im2.close()
            #print(np_im2)

            file2 = open("array2.txt", "a")
            file2.write(str(np_im2))
            file2.close()

            gif = generate_gif(app.config['GIF_FOLDER'])

            return render_template("index.html", filename=filepath, filename2=filepath2, gif=gif)

    return render_template("index.html", filename=filepath, gif=gif)


if __name__ == '__main__':
    app.run()
