from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired
from random import randint
from secret_key import SECRET_KEY

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = SECRET_KEY

user = None

class User():
    name = ""
    language = ""
    house = ""
    magic_item_level = ""

    def __init__(self, name='', language='', house='', magic_item_level=''):
        self.name = self.check_input(name)
        self.language = self.check_input(language)
        self.house = house
        self.magic_item_level = magic_item_level

    def check_input(self, param):
        # check if str
        if not isinstance(param, str):
            return ValueError("Parameter is not a string")
        elif not param.isascii():
            return Exception("String is not ASCII")
        return param

    def get_grade(self, level):
        if level < 4:
            self.magic_item_level = 'Low'
        elif level < 7:
            self.magic_item_level = 'Medium'
        else:
            self.magic_item_level = 'High'



class NameAndLanguageForm(FlaskForm):
    name = StringField('Enter your Name?', validators=[DataRequired(), Length(3, 30)])
    language = StringField('What is your Language?', validators=[DataRequired(), Length(3, 30)])
    submit = SubmitField('Next')

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
def name_and_language():
    form = NameAndLanguageForm()

    if form.validate_on_submit():
        global user
        user = User(form.name.data, form.language.data) #+

        return redirect(url_for('hogwarts_house'))
    return render_template('name_and_language.html', form=form)


@app.route("/hogwarts_house", methods=["GET", "POST"])
def hogwarts_house():
    form = HogwartsHouseForm()

    # Get the User instance from the request args
    global user

    if form.validate_on_submit():
        user = request.form.get("user")
        # Update the User instance with the selected house
        #house = form.category.data
        house = request.form.get("category") #POST #+

        """
        # Check on page skipping:
        if not user.name or not user.language:
            return redirect(url_for(('name_and_language')))
        """

        return redirect(url_for('magic_item'))
    return render_template('hogwarts_house.html', form=form)


@app.route("/magic_item", methods=["GET", "POST"])
def magic_item():
    form = MagicItemForm()

    # Get the User instance from the request args
    global user
    user = request.args.get('user')

    print(f"3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if form.validate_on_submit():
        print(f"4!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Set a random magic item level
        magic_item_level = randint(1, 10)
        user.get_grade(magic_item_level)
        print(f"5!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print(f"6 {user.magic_item_level}")
        print(f"7!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Display the user's info & suggest to Return:
        return  f"""
                <h3>Character Info:</h3>
                <ul>
                    <li>Name: {user.name}</li>
                    <li>Language: {user.language}</li>
                    <li>House: {user.house}</li>
                    <li>Magic Item Level: {user.magic_item_level}</li>
                </ul>
                <a href="/">Return to the HOME page</a>
            """
