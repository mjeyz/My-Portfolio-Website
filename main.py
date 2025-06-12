from flask import Flask, render_template, send_from_directory, request
from flask_bootstrap import Bootstrap
import smtplib
import dotenv
import os

app = Flask(__name__)
Bootstrap(app)
dotenv.load_dotenv()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Safely get values and provide defaults if missing
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        subject = request.form.get("subject", "")
        message = request.form.get("message", "")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("YOUR_GMAIL"), os.getenv("YOUR_PASSWORD"))
            email_message = f"Subject: {subject}\n\nName: {name}\nEmail: {email}\nMessage: {message}"
            server.sendmail(to_addrs=os.getenv("YOUR_GMAIL"), from_addr=os.getenv('YOUR_GMAIL'), msg=email_message)

    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download():
    return send_from_directory("static", path="files/Mudasir Abbas.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
