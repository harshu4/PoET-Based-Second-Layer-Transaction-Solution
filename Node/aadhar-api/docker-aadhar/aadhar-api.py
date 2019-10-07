import sqlite3
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

@app.route('/',methods=['POST'])
def respondant():
    if request.method=='POST' and request.files['image'] and request.args['aadharno']:
        image = request.files['image']
        aadharno = int(request.args['aadharno'])
        img_name = secure_filename(image.filename)

        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        image.save(saved_path)
        print(saved_path)
        image2  = get_image(int(aadharno))

        saved_path2 = "fig2.bmp"
        open(saved_path2,'wb').write(image2)
        arg = "java -jar match.jar "+img_name +" "+"fig2.bmp"
        p = os.popen(arg)
        time.sleep(1)
        arg2 = "rm -r " + img_name + "  fig2.bmp"
        r = os.popen(arg2)
        if p.read() == "true\n":
            return "true"
        else :
            return "false"
    else:
        return "data invalid"
def get_image(id):
    try:
        sqliteConnection = sqlite3.connect('aadhar.db')

        cursor = sqliteConnection.cursor()


        sql_fetch_blob_query = """SELECT * from PERSON where aadharno = ?"""
        cursor.execute(sql_fetch_blob_query, (id,))

        record = cursor.fetchall()
        for row in record:


            photo = row[4]

        return photo


        cursor.close()
    except sqlite3.Error as error:

        print("Error")

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False,port=7007)
