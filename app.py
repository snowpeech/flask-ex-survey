from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'whisper'

debug = DebugToolbarExtension(app)

responses=[]
#will replace q_num with len(responses)

@app.route('/')
def start_survey():
    """home page to start survey"""
    title=satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    responses=[]
    return render_template("instructions.html", survey_title=title, instructions=instructions)

@app.route('/questions/<int:q_num>')
def question_page(q_num):
    """ Show question of given number """
    title=satisfaction_survey.title
    question = satisfaction_survey.questions[q_num].question
    choices = satisfaction_survey.questions[q_num].choices

    return render_template("question.html", survey_title=title, question=question, choices=choices, q_num=q_num)

@app.route("/add-answer", methods=["POST"])
def add_answer():
    """Handle adding answer to response list."""

    ans = request.form['answer']
    responses.append(ans)
    
    # redirect...
    q_num = len(responses)
    
    if q_num == len(satisfaction_survey.questions):
        return render_template("thanks.html")
    else:
        return redirect(f"/questions/{q_num}")

    # return f'<h1>Received "{comment}".</h1>'