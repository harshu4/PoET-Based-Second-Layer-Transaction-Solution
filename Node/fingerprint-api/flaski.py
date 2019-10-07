from flask import Flask, url_for, send_from_directory, request
import logging, os
from werkzeug import secure_filename
import time
app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ['POST'])
def api_root():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image'] and request.files['image2']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img2 = request.files['image2']
        img_name = secure_filename(img.filename)
        img2_name = secure_filename(img2.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        saved_path2 = os.path.join(app.config['UPLOAD_FOLDER'], img2_name)
        app.logger.info("saving {}".format(saved_path))
        img2.save(saved_path2)
        img.save(saved_path)
        arg = "java -jar match.jar "+img_name +" "+img2_name
        p = os.popen(arg)
        time.sleep(1)
        arg2 = "rm -r " + img_name + " "+ img2_name
        r = os.popen(arg2)
        if p.read() == "true\n":
              return "true"
        else :
              return "false"
	
       
  	
    	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
