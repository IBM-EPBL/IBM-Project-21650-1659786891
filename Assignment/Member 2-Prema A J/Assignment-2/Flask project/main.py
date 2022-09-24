from flask import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('flaskindex.html')

@app.route('/signup')
def signup():
    return render_template('flasksignup.html')

@app.route('/login')
def sigin():
    return render_template('flasklogin.html')

@app.route('/about')
def blog():
    return render_template('flaskabout.html')


if __name__ == '__main__':
    app.run(debug=True)