
from flask import Flask, render_template
from markupsafe import escape
app = Flask(__name__)

numbList = []
b = 0

@app.route("/")
@app.route("/status")
def show_state():
    print(f"List status:{numbList}")
    return f"List status: {numbList}"
    #return render_template("status.html", ABC=numbList)


@app.route("/add")
def addition():
    global b
    b += 1
    numbList.append(b)
    print(f"List status:{numbList}")
    return f"List status: {numbList}"


@app.route("/del")
def addition():


if __name__ == '__main__':
    app.run()