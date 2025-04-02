from flask import Flask, render_template, request, redirect, flash
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

import hashlib

app = Flask(__name__)
# app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.sqlite'  # 혹은 MySQL 등으로 변경
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'

PORT = 3000 # Your Port >_0 -☆

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


def login(student_number, student_name, password):
    password = hashlib.sha256(password.encode()).hexdigest()
    if User.query.filter_by(userid=student_number).first():
        user = User.query.filter_by(userid=student_number).first()
        # login susccess
        if user.username == student_name and user.password == password:
            return True
        # login failed
        else:
            return False
    else:
        # signup success
        if signup(student_number, student_name, password):
            return True
        # signup failed
        else: return False
        
def signup(student_number, student_name, password):
    try:
        new_user = User(userid=student_number, username=student_name, password = password)
        
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
    
def save_score(student_number, score_value):
    """점수를 새로 저장 (기존 점수와 상관없이 무조건 추가)"""
    user = User.query.filter_by(userid=student_number).first()  # 학생 번호로 User 찾기
    if user:  
        new_score = Score(userid=user.userid, username=user.username, score=score_value)  # user.id 저장
        db.session.add(new_score)
        db.session.commit()
    else:
        print(f"User with student_number {student_number} not found.")

@app.route('/top_scores')
def get_top_scores():
    """점수가 높은 순서대로 상위 10개 반환 (학생별 최고 점수 기준)"""
    
    from sqlalchemy import func
    top_scores = db.session.query(
            Score.userid,
            Score.username,
            func.max(Score.score).label('score'),
            func.count().label('attempts')
        ).group_by(Score.userid)\
        .order_by(func.max(Score.score).desc())\
        .limit(10)
    
    score_list = [
        {
            "rank": idx + 1, 
            "student_id": s.userid, 
            "student_name": s.username,
            "score": round(s.score, 2),  # 퍼센트 변환
            "tries": Score.query.filter_by(userid=s.userid).count()  # 유저의 시도 횟수
        } 
        for idx, s in enumerate(top_scores)
    ]    

    return score_list

def get_current_ranking(student_number, score_value):
    '''
    @KimSummerRain
    current? No! 'colont'
    ㅋㅋㅋㅋㅋㅋㅋ
    '''
    """특정 점수에 대한 랭킹을 반환"""
    scores = Score.query.order_by(Score.score.desc()).all()
    # print(scores, score_value, student_number, type(student_number))
    rank = list(idx + 1 for idx, s in enumerate(scores) if s.userid == int(student_number) and s.score == score_value)[-1]
    # print(rank)
    return rank

# route
@app.route('/')
def index():
    # form = UploadForm()
    # return render_template('reviewform.html', form=form)
    return render_template('reviewform.html', rankings = get_top_scores())

@app.route('/results', methods=['POST'])
def results():
    # print('we posted')
    # form = UploadForm()
    # print(load(request.form))
    if request.method == 'POST' and 'answer' in request.files and request.files['answer'].filename != '':
        # print('fuck')
        
        student_number = request.form['student_id']
        condition = login(request.form['student_id'], request.form['student_name'], request.form['password'])
        
        if login(request.form['student_id'], request.form['student_name'], request.form['password']):
            # print(request.files)
            
            # save file
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y.%m.%d_%H-%M-%S')
            request.files['answer'].save(FILE_PATH + 'answers/'+request.form['student_id']+'_'+timestamp+'.csv')
            
            answer = np.loadtxt(FILE_PATH + 'answers/'+request.form['student_id']+'_'+timestamp+'.csv' , delimiter=',', skiprows=1, dtype=str)
            score = accuracy_score(correct, answer) * 100
            
            save_score(student_number,score)
            return render_template('results.html',
                                   student_name=request.form['student_name'],
                                    score=score,
                                    rank = get_current_ranking(student_number, score))
                                    # prediction=y,
                                    # probability=round(proba*100, 2))
        else: # login failed
            flash('비밀번호가 틀렸거나 이름이 틀립니다.')
            return redirect('/')
        
    return render_template('reviewform.html')
    # return render_template('reviewform.html', form=form)



if __name__ == '__main__':
    app.run(debug=True, port=PORT)