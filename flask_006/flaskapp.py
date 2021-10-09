from flask import Flask, render_template, request, redirect, url_for, session

from flask_006 import config
from flask_006.models import UserModel
from services import password_validation


app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key = config.SECRET_KEY


@app.before_request
def before_request():
    if 'is_logged' not in session:
        session['is_logged'] = False
        session['email'] = None
        session['password'] = None
        session.modified = True


def save_session_data(email):
    user = UserModel.get_objs(email=email)
    if 'remember' in request.form:
        session.permanent = True
        print('app.permanent = True')
    session['is_logged'] = True
    session['email'] = email
    session['password'] = user.password
    session.modified = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', is_logged=session['is_logged'], email=session['email'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['is_logged']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not UserModel.login(email, password):
            return render_template('login.html', default_email=email, default_password=password,
                                   login_error=True)
        save_session_data(email)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session['is_logged']:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not password_validation(password):
            return render_template('register.html', default_email=email, default_password=password,
                                   password_error=True)

        if UserModel.get_objs(email=email):
            return render_template('register.html', default_email=email, default_password=password,
                                   email_error=True)

        UserModel.register(email=email, password=password)
        save_session_data(email)
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout', methods=['GET'])
def logout():
    session['is_logged'] = False
    session['email'] = None
    session['password'] = None
    session.modified = True
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
