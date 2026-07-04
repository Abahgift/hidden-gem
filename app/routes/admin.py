from flask import render_template
from app import app

@app.route("/admin/login/", methods=["GET","POST"])
def admin_login():
    return render_template("admin/login.html", title="Login")

@app.route("/admin/analytics/")
def admin_analytics():
    return render_template("admin/analytics.html", title="Analytics")


@app.route("/admin/applications/")
def admin_applications():
    return render_template("admin/applications.html", title="Applications")


@app.route("/admin/guides/")
def admin_all_guides():
    return render_template("admin/all-guides.html", title="All Guides")


@app.route("/admin/destinations/")
def admin_destinations():
    return render_template("admin/destinations.html", title="Destinations")


@app.route("/admin/bookings/")
def admin_all_bookings():
    return render_template("admin/all-bookings.html", title="All Bookings")


@app.route("/admin/reviews/")
def admin_reviews():
    return render_template("admin/reviews.html", title="Reviews")