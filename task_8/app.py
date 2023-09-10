from flask import Flask, redirect, render_template, request, url_for, flash
from flask_wtf import CSRFProtect
from modelss import db, User, add_user
from formss import LoginForm, RegistrationForm, SubmitField



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

"""
>>> import secrets
>>> secrets.token_hex()
"""
app.config['SECRET_KEY'] = b'e87aca28a5d32fd1c5ec6108723b905809cea3e88a7f5d12a07e07a5b817aba3'

db.init_app(app)
csrf = CSRFProtect(app)

app.static_url_path = '/static'

@app.route('/', strict_slashes=False)
@app.route('/index.html', strict_slashes=False)
def index():
    return render_template('index.html')


@app.route('/odegda/', strict_slashes=False)
@app.route('/odegda.html/', strict_slashes=False)
def odegda():  # put application's code here
    return render_template('odegda.html')

@app.route('/vhod/', strict_slashes=False)
def vhod():
    return render_template('vhod.html')

@app.route('/obuv/', strict_slashes=False)
@app.route('/obuv.html/', strict_slashes=False)
def obuv():
    return render_template('obuv.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        add_user(first_name, last_name, email, password)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешно завершена! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/kurtka/')
def kurtka():
    return  render_template('kurtka.html')

@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('user_name', user_name)
        response.set_cookie('user_email', user_email)

        return response

@app.route('/welcome')
def welcome():
    user_name = request.cookies.get('user_name')
    return render_template('welcome.html', user_name=user_name)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')

    return response

@app.route('/news/')
def news():
    _news = [
        {
            "title": "John1",
            "descr": "Doe",
            "date": 201
        },
        {
            "title": "John2",
            "descr": "Doe",
            "date": 202
        },
        {
            "title": "John3",
            "descr": "Doe",
            "date": 203
        },
    ]
    context = {'news': _news}
    return render_template('news.html', **context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        pass
    return render_template('login.html', form=form)


@app.cli.command('init_db')
def init_db():
    db.create_all()
    print('OK')


def add_user(name, last_name, email, password):
    user = User(name, last_name, email, password)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    app.run()