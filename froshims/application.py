import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 2525
app.config["MAIL_SERVER"] = "smtp.mailtrap.io"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

db = SQL("sqlite:///froshims.db")

REGISTRANTS = {}

SPORTS = [
  "Dodgeball",
  "Flag Football",
  "Soccer",
  "Volleyball",
  "Ultimate Frisbee",
]

@app.route("/")
def index():
  return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
  email = request.form.get("email")
  if not email:
    return render_template("error.html", message="Missing email")

  sport = request.form.get("sport")
  if not sport:
    return render_template("error.html", message="Missing sport")
  if sport not in SPORTS:
    return render_template("error.html", message="Invalid sport")

  message = Message("You are registred!", recipients=[email])
  mail.send(message)

  return render_template("success.html")
