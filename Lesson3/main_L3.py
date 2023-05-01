from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired
from random import randint

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'secret_key'

class User():
    def __init__(self, name='', language='', house='', magic_item_level=0):
        self.name = name
        self.language = language
        self.house = house
        self.magic_item_level = magic_item_level

    def get_grade(self, level):
        if level < 4:
            self.magic_item_level = 'Low'
        elif level < 7:
            self.magic_item_level = 'Medium'
        else:
            self.magic_item_level = 'High'

class MyForm(FlaskForm):
    name = StringField('Enter your Name?', validators=[DataRequired(), Length(4, 30)])
    language = StringField('What is your Language?', validators=[DataRequired(), Length(3, 30)])
    category = RadioField('Choose your Hogwarts House:', validators=[InputRequired(message=None)],
            choices=[('griffindor', 'Griffindor'),
                        ('ravenclaw', 'Ravenclaw'),
                        ('hufflepuff', 'Hufflepuff'),
                        ('slytherin', 'Slytherin')])
    submit = SubmitField('Submit')

@app.route("/", methods=["GET", "POST"])
def show_items():
    form = MyForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        language = form.language.data
        house = form.category.data

        # create a new User object using the form data
        user = User(name, language, house)

        # set a random magic item level
        magic_item_level = randint(1, 10)
        user.get_grade(magic_item_level)

        # display the user's information
        return f"""
            <h3>Character Info:</h3>
            <ul>
                <li>Name: {user.name}</li>
                <li>Language: {user.language}</li>
                <li>House: {user.house}</li>
                <li>Magic Item Level: {user.magic_item_level}</li>
            </ul>
            <a href="/">Return to the HOME page</a>
        """

    return render_template('player.html', form=form)