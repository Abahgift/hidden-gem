from flask import render_template
from app import app

@app.route('/')
def landing_page():
    return render_template("traveler/homePage.html")