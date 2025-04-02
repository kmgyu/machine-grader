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


app = Flask(__name__)
app.secret_key = 'development key'

FILE_PATH = './'

correct = np.loadtxt(FILE_PATH + 'correct/correct.csv', delimiter=',', skiprows=1, dtype=str)


# def sqlite_entry(path, document, y):
#     conn = sqlite3.connect(path)
#     c = conn.cursor()
#     c.execute("INSERT INTO review_db (review, sentiment, date)"\
#     " VALUES (?, ?, DATETIME('now'))", (document, y))
#     conn.commit()
#     conn.close()

class UploadForm(FlaskForm):
    student_number = TextAreaField('Student Number',
                                [validators.DataRequired(),
                                validators.length(max=15)])
    answer = FileField('answer', validators=[ FileRequired(),
        FileAllowed(['csv'])])

# route
@app.route('/')
def index():
    form = UploadForm()
    return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    # print('we posted')
    form = UploadForm()
    # print(load(request.form))
    print(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        print(request.files)
        request.files['answer'].save(FILE_PATH + 'answers/'+request.form['student_number']+'.csv')
        answer = np.loadtxt(FILE_PATH + 'answers/'+request.form['student_number']+'.csv' , delimiter=',', skiprows=1, dtype=str)
        score = accuracy_score(correct, answer)
        
        return render_template('results.html',
                                score=score)
                                # prediction=y,
                                # probability=round(proba*100, 2))
    return render_template('reviewform.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)