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


class AlteringUserForm(FlaskForm):
    new_nickname = StringField('New nickname', validators=[DataRequired(), Length(3, 30)])
    new_password = StringField('New password', validators=[DataRequired(), Length(3, 30)])

    new_category = RadioField('Choose your Hogwarts House:', validators=[InputRequired(message=None)],
                          choices=[('Griffindor', 'Griffindor'),
                                   ('Ravenclaw', 'Ravenclaw'),
                                   ('Hufflepuff', 'Hufflepuff'),
                                   ('Slytherin', 'Slytherin')])

    submit = SubmitField('Update User Info')


usr_present = False


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    print("START ??????????????????????????????????")
    global usr_present
    l_form = LoginForm()
    # Create table
    sqlite_manager_L4.create_table()

    if l_form.validate_on_submit():
        user.nickname = l_form.nickname.data
        user.password = l_form.password.data

        # Check DB
        print(f"User Entered: {user.nickname}")
        usr_present = sqlite_manager_L4.check_user(user.nickname, user.password)
        print(f"User Present: {usr_present}")
        # SUBMIT
        if l_form.submit.data:
            if usr_present:
                print(f"Redirect to /magic. Show user from DB")
                return redirect(url_for('magic_item'))
            else:
                print(f"No such User in DB to Submit. Error Raise.")
                raise Exception("User is absent. Try to Register.")  # +
        # REGISTER
        elif l_form.register.data:
            if usr_present:
                print(f"Treat Existing user as login.To /magic")
                return redirect(url_for('magic_item'))
            else:
                print(f"To New User registration.")
                return redirect(url_for('register'))

    return render_template('login_form.html', form=l_form)


@app.route("/registration", methods=["GET", "POST"])
def register():
    global usr_present
    r_form = RegisterForm()

    if r_form.validate_on_submit():
        user.nickname = r_form.nickname.data
        user.password = r_form.password.data

        print(f"User that differs from /login but present in DB check.")
        usr_present = sqlite_manager_L4.check_user(user.nickname, user.password)
        print(f"User Present: {usr_present}")

        if usr_present:
            print("Trying to register Existing User")
            raise Exception("Nickname is taken. Try another one.")
        else:
            print(f"To house selection.")
            return redirect(url_for('hogwarts_house'))

    return render_template('register_form.html', form=r_form)


@app.route("/house", methods=["GET", "POST"])
def hogwarts_house():
    h_form = HogwartsHouseForm()

    if h_form.validate_on_submit():
        user.house = h_form.category.data
        print(f"HOUSE: {user.house}")
        print(f"To Last Page.")
        return redirect(url_for('magic_item'))

    return render_template('hogwarts_house_L4.html', form=h_form, nickname=user.nickname, password=user.password)


@app.route("/item", methods=["GET", "POST"])
def magic_item():
    global usr_present
    m_form = MagicItemForm()

    # Set a random magic item level
    print(f"MIL before: {user.magic_item_level}")
    magic_item_level = randint(1, 10)
    user.get_grade(magic_item_level)
    print(f"MIL after: {user.magic_item_level}")

    if usr_present:
        print(f"Show User from DB")
        all_info = sqlite_manager_L4.get_all_info(user.nickname, user.password)
        print(f"ALL INFO: {all_info}")
        # Set all User info according to DB:
        user.nickname, user.password, user.house, user.magic_item_level = all_info

    else:
        print("Put new User in DB")
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
            <br>
            <a href="/alter">Change User Info</a>
        """


@app.route("/alter", methods=["GET", "POST"])
def alter_user_info():
    alter_form = AlteringUserForm()

    if alter_form.validate_on_submit():
        print("About to DEL")
        sqlite_manager_L4.del_user_info(user.nickname)

        user.nickname = alter_form.new_nickname.data
        user.password = alter_form.new_password.data
        user.house = alter_form.new_category.data
        user.get_grade(randint(1, 10))

        print("Pre ALTER")
        # Update DB
        sqlite_manager_L4.put_user_info(user.nickname, user.password, user.house, user.magic_item_level)
        # redirect the user to the magic item page
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return redirect(url_for('magic_item'))
        # check usr_present var!!!!!!!!!

    return render_template('alter_user_info.html', form=alter_form, nickname=user.nickname, password=user.password, house=user.house, magic_item_level=user.magic_item_level)



if __name__ == "__main__":
    try:
        conn = sqlite3.connect("user_L4.db")
    finally:
        conn.close()
    app.run(host='0.0.0.0', port='8000', debug=True)
