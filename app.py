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

#app.config['GIF_FOLDER1_Colored'] = "static/GIF_FOLDER1_Colored/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_gif(directory):

    files = os.listdir(directory)
    array = []

    #for file in files:
    #    if "gif" in file:
    #        print("Gif file :"+file)
    #    else:
    #        img1 = Image.open(directory+file)
    #        array.append(img1)
    #        print("Image File: "+file)
    for i in range (7):
        filename = "img" + str(i) + ".jpg"
        img = Image.open (directory + filename)
        array.append (img)

    #gif = Image.new('RGB', (1200, 1200))

    #gif.save(directory+'out.gif', save_all=True, append_images=array, duration=1000, loop=0)
    array[0].save (directory+'out.gif', save_all=True, append_images=array, duration=1000, loop=0)
    return directory+'out.gif'

def colorate(matrizoriginal,matrizdecolorada):
    for i in range(len(matrizdecolorada)):
        for y in range(len(matrizdecolorada[i])):
            matrizdecolorada[i][y] = matrizoriginal[i][y]
    file1color = open("arraycolor2.txt", "a")
    file1color.write(str(matrizdecolorada))
    file1color.close()
    return matrizdecolorada



@app.route('/', methods=['GET', 'POST'])
def upload_image():
    filepath = "no"
    gif1 = "no"
    gif2 = "no"
    gif3 = "no"
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
            #imcolor = im.convert('RGB')
            #np_imcolor=numpy.array(imcolor)
            imgblack = im.convert('1')
            np_im = numpy.array(imgblack)
            im.close()
            # print(np_im)

            #file1 = open("array.txt", "a")
            #file1.write(str(np_im))
            #file1.close()

            #file1color = open("arraycolor.txt", "a")
            #file1color.write(str(np_imcolor))
            #file1color.close()

            im2 = Image.open(filepath2)
            imgblack2 = im2.convert('1')
            np_im2 = numpy.array(imgblack2)
            im2.close()
            #print(np_im2)
            
            #arrayimagenes = trans.generate_animation(np_im.tolist(), np_im2.tolist(), trans.greedy_trans(np_im.tolist(), np_im2.tolist()))
            #print ("finished greedy")
            arrayimagenes2 = trans.generate_animation(np_im.tolist(), np_im2.tolist(), trans.dp_trans(np_im.tolist(), np_im2.tolist()))
            #arrayimagenes3 = trans.generate_animation(np_im.tolist(), np_im2.tolist(), trans.dp_trans_avg(np_im.tolist(), np_im2.tolist()))
            Imagen = Image.fromarray(np_im)
            Imagen.save (app.config['GIF_FOLDER2'] + "img" + str(0) + ".jpg")
            for i in range(1, 6):
                #imagen=Image.fromarray(numpy.array(arrayimagenes[i]))
                #imagen.save(app.config['GIF_FOLDER1']+"img"+str(i)+".jpg")
                imagen = Image.fromarray(numpy.array(arrayimagenes2[i]))
                imagen.save(app.config['GIF_FOLDER2'] + "img" + str(i) + ".jpg")
                #imagen = Image.fromarray(numpy.array(arrayimagenes3[i]))
                #imagen.save(app.config['GIF_FOLDER3'] + "img" + str(i) + ".jpg")
                #imagencolorada=Image.fromarray(numpy.array(colorate(np_imcolor.tolist(), arrayimagenes[i])))
                #imagencolorada.save(app.config['GIF_FOLDER1_Colored']+"img"+str(i)+".jpg")
            Imagen = Image.fromarray(np_im2)
            Imagen.save (app.config['GIF_FOLDER2'] + "img" + str(6) + ".jpg")
            #file2 = open("array2.txt", "a")
            #file2.write(str(np_im2))
            #file2.close()

            #gif1 = generate_gif(app.config['GIF_FOLDER1'])
            gif2 = generate_gif(app.config['GIF_FOLDER2'])
            #gif3 = generate_gif(app.config['GIF_FOLDER3'])

            return render_template("index.html", filename=filepath, filename2=filepath2, gif2=gif2)

    return render_template("index.html", filename=filepath, gif2=gif2)


if __name__ == '__main__':
    app.run()
