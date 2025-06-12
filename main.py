from flask import Flask, render_template, url_for, send_from_directory
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=['GET', 'POST'])
def download():
    return send_from_directory("static", path="files/Mudasir Abbas.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5003)