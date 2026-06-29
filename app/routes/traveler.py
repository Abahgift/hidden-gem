from flask import render_template
from app import app

@app.route("/")
def landing_page():
    return render_template("traveler/homePage.html")

@app.route("/signup/")
def signup():
    return render_template("traveler/signUp.html")


@app.route("/login/")
def login():
    return render_template("traveler/login.html")


@app.route("/otp/", methods=["GET","POST"])
def otp():
    return render_template("traveler/otp.html")


@app.route("/dashboard/", methods=["GET", "POST"])
def dashboard():
    return render_template("traveler/dashboard.html")