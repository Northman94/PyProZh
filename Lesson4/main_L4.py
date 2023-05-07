
from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired
from random import randint
from secret_key_L4 import SECRET_KEY

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


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    l_form = LoginForm()

    if l_form.validate_on_submit():
        user.name = l_form.nickname.data
        user.password = l_form.password.data
        # rethink if this should be here ^
        if l_form.submit.data:
            pass
            # if user present in DB - show last page
            #  elif not - Show Error. Suggest Register or try again
        elif l_form.register.data:
            return redirect(url_for('registration'))

    return render_template('login_form.html', form=l_form)

@app.route("/registration", methods=["GET", "POST"])
def register():
    r_form = RegisterForm()

    if r_form.validate_on_submit():
        user.name = r_form.nickname.data
        user.password = r_form.password.data
        if r_form.submit.data:
            pass

    # if nickname present in DB - Error
    #  elif not - create a new User (Register)
        # return redirect(url_for('hogwarts_house'))

    return render_template('register_form.html', form=r_form)


@app.route("/hogwarts_house", methods=["GET", "POST"])
def hogwarts_house():
    h_form = HogwartsHouseForm()

    # Check on page skipping:
    if not user.nickname or not user.password:
        return redirect(url_for(('login')))
    print(user.nickname)
    print(user.password)

    if h_form.validate_on_submit():

        user.house = h_form.category.data
        return redirect(url_for('magic_item'))

    return render_template('hogwarts_house_L4.html', form=h_form, name=user.nickname, language=user.password)


@app.route("/magic_item", methods=["GET", "POST"])
def magic_item():
    m_form = MagicItemForm()

    # Check on page skipping:
    if not user.nickname or not user.password:
        return redirect(url_for(('login')))
    elif not user.house:
        return redirect(url_for(('hogwarts_house')))

    # Set a random magic item level
    magic_item_level = randint(1, 10)
    user.get_grade(magic_item_level)

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
