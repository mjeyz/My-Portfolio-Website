from flask import Flask, render_template, send_from_directory, request
from flask_bootstrap import Bootstrap5
import smtplib
import dotenv
import os
import psycopg2


app = Flask(__name__)
Bootstrap5(app)
dotenv.load_dotenv()
app.config["SECRET_KEY"] = "cvdsg3456w7w3456gh"
DATABASE_URL = "postgresql://postgres:9992@localhost:5432/portfolio"

conn = psycopg2.connect(DATABASE_URL)


with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitor (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            subject VARCHAR(150) NOT NULL,
            message VARCHAR(150) NOT NULL
        )
    """)
    conn.commit()


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


        with conn.cursor() as cur:
            cur.execute("INSERT INTO visitor (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                        (name, email, subject, message))
            conn.commit()

    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download():
    return send_from_directory("static", path="files/Mudasir Abbas.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
