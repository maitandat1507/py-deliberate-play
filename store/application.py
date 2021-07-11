import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

# DB config
db = SQL("sqlite:///stores.db")

# Session configuration
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
  books = db.execute("SELECT * FROM books")
  return render_template("books.html", books=books)

@app.route("/cart", methods=["GET", "POST"])
def cart():
  # Ensure cart exists
  if "cart" not in session:
    session["cart"] = []
  
  # POST
  if request.method == "POST":
    id = request.form.get("book_id")
    if id:
      session["cart"].append(id)
      return redirect("/cart")

  # GET
  if request.method == "GET":
    books = db.execute("SELECT * FROM books WHERE id IN (?)", session["cart"])
    return render_template("cart.html", items=books)
