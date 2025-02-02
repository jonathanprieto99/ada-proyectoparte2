from flask import Flask, request, redirect, render_template
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy
import sys
import trans

numpy.set_printoptions(threshold=sys.maxsize)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

#app.secret_key = os.environ.get('SECRET_KEY')
#app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
#app.config['GIF_FOLDER1'] = os.environ.get('GIF_FOLDER1')

app.secret_key = "SECRETKEYFORGUTECIMAGE"
app.config['UPLOAD_FOLDER'] = "static/upload"
app.config['GIF_FOLDER1'] = "static/GIF_FOLDER1/"
app.config['GIF_FOLDER2'] = "static/GIF_FOLDER2/"
app.config['GIF_FOLDER3'] = "static/GIF_FOLDER3/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_gif(directory):

    array = []

    for i in range(7):
        filename = "img" + str(i) + ".jpg"
        img = Image.open(directory+filename)
        array.append(img)
        print("Image File: "+filename)

    gif = Image.new('RGB', (200, 200))
    gif.save(directory+'out.gif', save_all=True, append_images=array, duration=1000, loop=0)

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

            #file1 = open("array.txt", "a")
            #file1.write(str(np_im))
            #file1.close()

            im2 = Image.open(filepath2)
            imgblack2 = im2.convert('1')
            np_im2 = numpy.array(imgblack2)
            im2.close()
            #print(np_im2)

            algoritmo = request.form['algoritmo']

            if algoritmo == "GREEDY":
            
                arrayimagenes = trans.generate_animation(np_im.tolist(), np_im2.tolist(), trans.greedy_trans(np_im.tolist(), np_im2.tolist()))

                for i in range(7):
                    imagen = Image.fromarray(numpy.array(arrayimagenes[i]))
                    imagen.save(app.config['GIF_FOLDER1'] + "img" + str(i) + ".jpg")
                gif = generate_gif(app.config['GIF_FOLDER1'])

            elif algoritmo == "ProgDinamica 1":

                arrayimagenes2 = trans.generate_animation(np_im.tolist(), np_im2.tolist(), trans.dp_trans(np_im.tolist(), np_im2.tolist()))

                for i in range(7):
                    imagen = Image.fromarray(numpy.array(arrayimagenes2[i]))
                    imagen.save(app.config['GIF_FOLDER2'] + "img" + str(i) + ".jpg")
                gif = generate_gif(app.config['GIF_FOLDER2'])

            else:

                arrayimagenes3 = trans.generate_animation(np_im.tolist(), np_im2.tolist(), trans.dp_trans_avg(np_im.tolist(), np_im2.tolist()))

                for i in range(7):

                    imagen = Image.fromarray(numpy.array(arrayimagenes3[i]))
                    imagen.save(app.config['GIF_FOLDER3'] + "img" + str(i) + ".jpg")
                gif = generate_gif(app.config['GIF_FOLDER3'])

            return render_template("index.html", filename=filepath, filename2=filepath2, gif=gif, algoritmo=algoritmo)

    return render_template("index.html", filename=filepath, gif=gif)


if __name__ == '__main__':
    app.run()
