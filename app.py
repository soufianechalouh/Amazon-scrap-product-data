import os

from flask import Flask, request, render_template, send_from_directory

import amzn

UPLOAD_FOLDER = './tmp/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
__location__ = os.path.realpath(
   os.path.join(os.getcwd(), os.path.dirname(__file__)))

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/download', methods=['GET', 'POST'])
def upload_file():
    print("we're inside")
    target = './tmp/uploads'
    if not os.path.isdir(target):
        os.makedirs(target)
        print("'re inside")

    if request.method == 'POST':
        print("method")

        file = request.files['the_file']
        print('did we get it')
        file_name = file.filename or ''
        destination = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(destination)
        print(file_name)

        return amzn.get_assins(file_name)
    return "no congrats"


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory('tmp/downloads', filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
