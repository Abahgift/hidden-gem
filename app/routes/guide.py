from flask import render_template
from app import app


@app.route("/guide/dashboard/")
def guide_dashboard():
    return render_template(
        "guide/dashboard.html",
        title="Dashboard",
        current_page="dashboard",
    )


@app.route("/guide/bookings/")
def guide_bookings():
    return render_template(
        "guide/bookings.html",
        title="Bookings",
        current_page="bookings",
    )


@app.route("/guide/profile/")
def guide_profile():
    return render_template(
        "guide/my_profile.html",
        title="Profile",
        current_page="profile",
    )


@app.route("/guide/trails/")
def guide_trails():
    return render_template(
        "guide/my_trails.html",
        title="My Trails",
        current_page="trails",
    )


@app.route("/guide/reviews/")
def guide_reviews():
    return render_template(
        "guide/reviews.html",
        title="Reviews",
        current_page="reviews",
    )