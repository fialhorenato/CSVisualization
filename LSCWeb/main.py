import os
from flask import Flask,render_template,request,redirect, url_for
import generator as gen

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.debug = True

@app.route('/',methods=['GET'])
def index():
        return render_template('analyse.html')

@app.route('/',methods=['POST'])
def index2():
    file = request.files['datafile']
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        gen.generateJSON(file.filename)
    return render_template('analyse.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
