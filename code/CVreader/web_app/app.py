#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, redirect, url_for, session, flash, render_template, request
import urllib.request
from werkzeug import secure_filename
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

import os, tempfile

from skillator import Skillator
from gensim.models import FastText
import itertools

app = Flask(__name__)
app.secret_key = "secret key"

app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['CV_FILE'] = ''


ALLOWED_EXTENSIONS = set(['pdf', 'docx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.config['CV_FILE'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash('File successfully uploaded')
            return redirect(url_for('success'))
    else:
        flash('Allowed file types are pdf or docx')
        return redirect(request.url)

@app.route('/success')
def success():
    skill_class = Skillator(app.config['CV_FILE'])
    name, cv_skills = skill_class.skill_extraction(os.path.join(skill_class.rootDir, skill_class.cv))
    
    session['name'] = name
    session['rootDir'] = skill_class.rootDir
    normalized_skills = skill_class.skills_from_file(os.path.join(skill_class.rootDir, skill_class.skill_file))

    cv_skills = skill_class.skill_normalization(cv_skills, normalized_skills)
    #cv_skills = ['angular', 'azure', 'c', 'css', 'data_structures', 'excel', 'git', 'html', 'javascript', 'laravel', 'linux', 'machine_learning', 'mongodb', 'nlp', 'php', 'python', 'scrum', 'unix']
    skill_list = [i.replace('_', ' ') for i in set([i.capitalize() for i in cv_skills])]

    return render_template('hello.html', user = name, skills = skill_list)


@app.route('/success', methods=['POST'])
def my_form_post():
    name = session.get('name', None)
    if request.method == 'POST':
        skills = []
        for key, value in request.form.items():
            skills.append(value)
    session['cv_skills'] = skills
    rootDir = session.get('rootDir', None)

    model = FastText.load(os.path.join( rootDir+'/model', 'word2vec.model'))

    final_rec = []
    cv_skills = [i.replace(' ', '_') for i in set([i.lower() for i in skills])]

    for skill in cv_skills:
        try:
            recommended_skills = model.similar_by_vector(model[skill], topn= 6+1)[1:]
            final_list = [skill[0] for skill in recommended_skills if skill[0] not in cv_skills and skill[0] not in final_rec and skill[1] > 0.90]
            if len(final_list) != 0 : final_rec.append(final_list)
        except KeyError:
            pass

    final_rec = list(itertools.chain.from_iterable(final_rec))
    final_rec = [i.replace('_', ' ') for i in set([i.capitalize() for i in final_rec])]
    return render_template('output.html', user = name, skills = [i for i in skills if len(i) != 0], rec_skills = final_rec)

@app.route('/profil_validation')
def profil_validation():
    return render_template('profil.html')

@app.route('/profil_validation', methods=['POST'])
def skill_post():
    name = session.get('name', None)
    cv_skills = session.get('cv_skills', None)
    
    if request.method == 'POST':
        for key, value in request.form.items():
            cv_skills.append(value)

    return render_template('profil.html', user = name, skills = [i for i in cv_skills if len(i) != 0] )



if __name__ == '__main__':

    app.run(debug=True)
