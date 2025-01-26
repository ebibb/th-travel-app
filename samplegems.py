from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/gems")
def gems_page():
    with open("gems.json", "r") as file:
        gems = json.load(file)
    return render_template("gems.html", gems=gems)

if __name__ == "__main__":
    app.run(debug=True)
