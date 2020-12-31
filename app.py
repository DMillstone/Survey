from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


answers = []

@app.route('/')
def say_hello():
    survey = surveys["satisfaction"]
    if len(survey.questions) == len(answers):
        return redirect('/thankyou')
    elif len(answers) > 0:
        flash('Please do not try to skip ahead or go back.')
        return redirect(f'/questions/{len(answers)}')
    else:
        return render_template("home.html",
                            title=survey.title,
                            instructions=survey.instructions)

@app.route('/questions/<index>')
def print_survey(index):
    index = int(index)
    survey = surveys["satisfaction"]
    if index != len(answers):
        flash('Please do not try to skip ahead or go back.')
        return redirect(f'/questions/{str(len(answers))}')
    elif len(survey.questions) == len(answers):
        return redirect('/thankyou')
    else:
        return render_template("question.html",
                            title=survey.title,
                            instructions=survey.instructions,
                            question=survey.questions[index].question,
                            choices=survey.questions[index].choices)
                            

@app.route('/thankyou')
def thank_you():
    return render_template("thankyou.html")

@app.route('/answer')
def record_answer():
    answer = request.args["answer"]
    answers.append(answer)
    index = len(answers)
    survey = surveys["satisfaction"]
    if index < len(survey.questions):
        return redirect(f'/questions/{index}')
    else: 
        return redirect('/thankyou')




