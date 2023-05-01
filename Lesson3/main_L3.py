
from flask import Flask, request
from random import randint

app = Flask(__name__)


class User():
    name = ''  # validation ascii
    language = ''
    house = ''
    magic_item_level = ''

    def __init__(self, name='', language=''):
        self._name = name
        self.language = language

    def choose_house(self, house):
        self.house = house

    def get_grade(self, magic_item_level):
        self.magic_item_level = magic_item_level


@app.route("/")
def show_items(state_list=None):
    return f"""
<h3>Character Info: {state_list}</h3>

<form action="/add_item" method="POST">
    
<br><br>

    <label for="name">Your Name:</label>
    <input type="text" id="name" name="name" required minlength="4" maxlength="20" size="10">
       
<br><br>   
    
    <label for="name">Your Language:</label>
    <input type="text" id="name" name="name" required minlength="4" maxlength="15" size="10">
       
<br><br>  
     
        <fieldset>
    <legend>Your Hogwarts House:</legend>

    <div>
      <input type="radio" id="gryffindor" name="drone" value="gryffindor"
             checked>
      <label for="gryffindor">Gryffindor</label>
    </div>

    <div>
      <input type="radio" id="ravenclaw" name="drone" value="ravenclaw">
      <label for="ravenclaw">Ravenclaw</label>
    </div>

    <div>
      <input type="radio" id="hufflepuff" name="drone" value="hufflepuff">
      <label for="hufflepuff">Hufflepuff</label>
    </div>
    
    <div>
      <input type="radio" id="slytherin" name="drone" value="slytherin">
      <label for="slytherin">Slytherin</label>
    </div>
</fieldset>

<br><br>
        
    <div>
        <label for="new_item">
            You found a Phoenix feather. Submit Data to see it's rarity.
        </label>
<br><br>    
    </div>
      
<br><br>

    <button>Submit Data</button>
    
</form>
    """


@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form['name']
    language = request.form['language']
    house = request.form['drone']

    # create a new User object using the form data
    user = User(name, language)
    user.choose_house(house)

    # set a random magic item level
    magic_item_level = randint(1, 10)
    user.get_grade(magic_item_level)

    # display the user's information
    return f"""
        <h3>Character Info:</h3>
        <ul>
            <li>Name: {user._name}</li>
            <li>Language: {user.language}</li>
            <li>House: {user.house}</li>
            <li>Magic Item Level: {user.magic_item_level}</li>
        </ul>
        <a href="/">Return to the HOME page</a>
    """


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)




"""
button = document.querySelector('input')
paragraph = document.querySelector('p')

button.addEventListener('click', updateButton)

function updateButton() {
  if (button.value === 'Start machine') {
    button.value = 'Stop machine';
    paragraph.textContent = 'The machine has started!'
  } elif {
    button.value = 'Start machine'
    paragraph.textContent = 'The machine is stopped.'
  }
}
"""