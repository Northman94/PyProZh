
from flask import Flask, render_template
app = Flask(__name__)

numbList = []
b = 0


@app.route("/")
@app.route("/status", methods = ["GET"])
def show_state():
    print(f"List status:{numbList}")
    #return f"List status: {numbList}"
    return render_template("status.html", numbList=numbList)


@app.route("/add", methods = ["GET", "POST"])
def addition():
    global b
    b += 1
    numbList.append(b)
    print(f"List status:{numbList}")
    #return f"List status: {numbList}"
    return render_template("addition.html", addList=numbList)


@app.route("/del", methods = ["GET","DELETE"])
def delete():
    print(len(numbList))
    if len(numbList) >= 1:
        numbList.pop()
    #return f"List status: {numbList}"
        return render_template("delete.html", delList=numbList)
    else:
        return render_template("status.html", numbList=numbList)


if __name__ == '__main__':
    app.run()
