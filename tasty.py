from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import TextAreaField, validators
# import pickle
import sqlite3
import os
import numpy as np
# from vectorizer import vect
from sklearn.metrics import accuracy_score
from models import db, User, Score

app = Flask(__name__)
# app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.sqlite'  # 혹은 MySQL 등으로 변경
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'


db.init_app(app)

# 첫 실행 시에만 실행
with app.app_context():
    db.create_all()

FILE_PATH = './'

correct = np.loadtxt(FILE_PATH + 'correct/correct.csv', delimiter=',', skiprows=1, dtype=str)


def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO review_db (review, sentiment, date)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()


def login(student_number, password):
    if User.query.filter_by(userid=student_number).first():
        user = User.query.filter_by(userid=student_number).first()
        # login susccess
        if user.password == password:
            return True
        # login failed
        else:
            return False
    else:
        # signup success
        if signup(student_number, password):
            return True
        # signup failed
        else: return False
        
def signup(student_number, password):
    try:
        new_user = User(userid=student_number, password = password)
        
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
    return False

class UploadForm(FlaskForm):
    student_number = TextAreaField('Student Number',
                                [validators.DataRequired(),
                                validators.length(max=15)])
    answer = FileField('answer', validators=[ FileRequired(),
        FileAllowed(['csv'])])

# route
@app.route('/')
def index():
    # form = UploadForm()
    # return render_template('reviewform.html', form=form)
    return render_template('reviewform.html')

@app.route('/results', methods=['POST'])
def results():
    # print('we posted')
    # form = UploadForm()
    # print(load(request.form))
    if request.method == 'POST' and request.files:
        print('fuck')
        if login(request.form['student_id'], request.form['password']):
            # print(request.files)
            request.files['answer'].save(FILE_PATH + 'answers/'+request.form['student_id']+'.csv')
            answer = np.loadtxt(FILE_PATH + 'answers/'+request.form['student_id']+'.csv' , delimiter=',', skiprows=1, dtype=str)
            score = accuracy_score(correct, answer)
            
            return render_template('results.html',
                                    score=score)
                                    # prediction=y,
                                    # probability=round(proba*100, 2))
        
    return render_template('reviewform.html')
    # return render_template('reviewform.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)