from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired
from secret_key_L4 import SECRET_KEY
from random import randint
import sqlite3
import sqlite_manager_L4

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = SECRET_KEY


class User():
    def __init__(self, nickname='', password='', house='', magic_item_level=''):
        self.nickname = self.check_input(nickname)
        self.password = self.check_input(password)
        self.house = house
        self.magic_item_level = magic_item_level

    def check_input(self, param):
        # check if str
        if not isinstance(param, str):
            raise ValueError("Parameter is not a string")
        elif not param.isascii():
            raise Exception("String is not ASCII")
        return param

    def get_grade(self, level):
        if level < 4:
            self.magic_item_level = 'Low'
        elif level < 7:
            self.magic_item_level = 'Medium'
        else:
            self.magic_item_level = 'High'


user = User()


class LoginForm(FlaskForm):
    nickname = StringField('Enter your Login.', validators=[DataRequired(), Length(3, 30)])
    password = StringField('Enter Password.', validators=[DataRequired(), Length(3, 30)])
    submit = SubmitField('Submit')
    register = SubmitField('Register new User')


class RegisterForm(FlaskForm):
    nickname = StringField('Enter your Login.', validators=[DataRequired(), Length(3, 30)])
    password = StringField('Enter Password.', validators=[DataRequired(), Length(3, 30)])
    submit = SubmitField('Submit new User')


class HogwartsHouseForm(FlaskForm):
    category = RadioField('Choose your Hogwarts House:', validators=[InputRequired(message=None)],
                          choices=[('Griffindor', 'Griffindor'),
                                   ('Ravenclaw', 'Ravenclaw'),
                                   ('Hufflepuff', 'Hufflepuff'),
                                   ('Slytherin', 'Slytherin')])

    submit = SubmitField('Next')


class MagicItemForm(FlaskForm):
    submit = SubmitField('Get Your Magic Item')


usr_present = None


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    get_all_info = False

    l_form = LoginForm()
    # Create table
    sqlite_manager_L4.create_table()

    if l_form.validate_on_submit():
        user.name = l_form.nickname.data
        user.password = l_form.password.data

        # Check DB
        global usr_present
        usr_present = sqlite_manager_L4.get_user_info(user.name, user.password, get_all_info)
        print(f"User Present: {usr_present}")

        if l_form.submit.data:
            if usr_present:
                return redirect(url_for('magic_item'))
            else:
                raise Exception("User is absent. Try to Register.")  # +

        elif l_form.register.data:
            if usr_present:
                # Treat Existing user as login
                return redirect(url_for('magic_item'))
            else:
                return redirect(url_for('register'))

    return render_template('login_form.html', form=l_form)


@app.route("/registration", methods=["GET", "POST"])
def register():
    r_form = RegisterForm()

    if r_form.validate_on_submit():
        user.name = r_form.nickname.data
        user.password = r_form.password.data

        # User that differs from /login but present in DB check:
        global usr_present
        usr_present = sqlite_manager_L4.get_user_info(user.name)
        print(f"User Present: {usr_present}")

        if usr_present:
            raise Exception("Nickname is taken. Try another one.")
        else:
            return redirect(url_for('hogwarts_house'))

    return render_template('register_form.html', form=r_form)


@app.route("/house", methods=["GET", "POST"])
def hogwarts_house():
    h_form = HogwartsHouseForm()

    # Check on page skipping:
    page_skipping_check()

    if h_form.validate_on_submit():
        user.house = h_form.category.data
        return redirect(url_for('magic_item'))

    return render_template('hogwarts_house_L4.html', form=h_form, name=user.nickname, language=user.password)


@app.route("/item", methods=["GET", "POST"])
def magic_item():
    global usr_present
    get_all_info = True

    m_form = MagicItemForm()

    # Check on page skipping:
    page_skipping_check()

    # Set a random magic item level
    magic_item_level = randint(1, 10)
    user.get_grade(magic_item_level)



    if usr_present:
        # Get User from DB
        db_content = sqlite_manager_L4.get_user_info(user.nickname, user.password, get_all_info)
        print('6!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(db_content)
        user.nickname = db_content[0]
        user.password = db_content [1]
        user.house = db_content[2]
        user.magic_item_level = db_content[3]

    else:
        # Put new User in DB
        sqlite_manager_L4.put_user_info(user.nickname, user.password, user.house, user.magic_item_level)

    # Display the user's info & suggest to Return:
    return f"""
           <h3>Character Info:</h3>
            <ul>
                <li>Name: {user.nickname}</li>
                <li>Password: {user.password}</li>
                <li>House: {user.house}</li>
                <li>Magic Item Level: {user.magic_item_level}</li>
            </ul>
            <a href="/">Return to the HOME page</a>
        """


def page_skipping_check():
    if not user.nickname or not user.password:
        return redirect(url_for('login'))
    elif not user.house:
        return redirect(url_for('house'))


if __name__ == "__main__":
    try:
        conn = sqlite3.connect("user_L4.db")
    finally:
        conn.close()
    app.run(host='0.0.0.0', port='8000', debug=True)
