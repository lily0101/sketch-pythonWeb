# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:38:04 2017

@author: lily0101
"""
import os
import json
from flask import redirect, url_for
from werkzeug import secure_filename
from flask import Flask, request, render_template
from flask import send_from_directory,jsonify
import numpy as np
import matplotlib as plt
import matplotlib.image as mpimg
from skimage.feature import match_template

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'data')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
all_data = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def templateMatch():
    image = mpimg.imread(os.path.join(app.config['UPLOAD_FOLDER'], "student.png"))
    template = mpimg.imread(os.path.join(app.config['UPLOAD_FOLDER'], "origin.png"))
    result = match_template(image,template)
    return result

@app.route('/student',methods=['GET','POST'])
def student():
    if request.method == 'POST': # return the student drawing UI
        upload_files = request.files.getlist('image')
        name = ""
        for file in upload_files:
            print(file)
            if file and allowed_file(file.filename):
                name = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        #return the score of two images
        score = templateMatch()
        print(score[0][0][0])
        return jsonify(score[0][0][0])
    return render_template('student.html')


@app.route('/teacher',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        #print("get the file?")
        data = json.loads(request.get_data())
        postName = "strokes";
        if postName in data:
            strokes = data["strokes"]
            print(strokes)
            filename = os.path.join(app.config['UPLOAD_FOLDER'],data['name']);
            np.save(filename+'.npy',strokes)
            all_data.append(strokes)
            return "success";
        else:
            #save it to file
            print("save it to file")
            filename = os.path.join(app.config['UPLOAD_FOLDER'],data['name']);
            np.save(filename+'.npy',all_data)
            all_data = []

        '''
        #code in below is for image of canvas
        file = request.files['image']
        print(file)
        if file and allowed_file(file.filename):
            print("what't wrong with the img")
            filename = secure_filename(file.filename)            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #save the file
            return redirect(url_for('uploaded_file',  
                                    filename=filename))
        '''

    return render_template('teacher.html')

#for the return file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def home_page():
    return render_template('first.html')

@app.route('/addnumber')
def add():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    return jsonify(result=a + b)


@app.route('/login', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username=='teacher' and password=='password':
        return render_template('teacher.html', username=username)
    elif username == 'student' and password == "password":
        return render_template('student.html',username=username)
    #failed
    return render_template('login_failed.html', message='Wrong username or password', username=username)



if __name__ == '__main__':
    app.debug = True
    app.run()
