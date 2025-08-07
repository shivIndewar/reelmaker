from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os
import generate_process

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        rec_id = request.form.get('myid')
        desc = request.form.get('text')
        input_files =[]
        print(request.files.keys())
        for key, value in request.files.items():
            print(key, value)
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if(not (os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id)))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, filename))
                input_files.append(filename)
                print(f"File {filename} saved successfully.")
                with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
                    f.write(desc)
                print(f"Description saved successfully for {rec_id}.")
    
        for fl in input_files:
            print(f"File {file} uploaded successfully.")
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "a") as f:
                f.write(f"file {fl} \n duration 1\n")
    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    reels = os.listdir('static/reels')
    return render_template("gallery.html", reels=reels)

app.run(debug=True)