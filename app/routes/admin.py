import os
from flask import render_template, request, url_for, flash, session, redirect
from app import app
from app.utils.auth_helpers import admin_required, check_admin_credentials



@app.route("/admin/login/", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        check = check_admin_credentials(email, password)

        if check:
            session["is_admin"] = True
            return redirect(url_for('admin_analytics'))
        else:
            flash("Invalid credentials")
            return render_template("admin/login.html", title="Admin Login")

    # GET request
    return render_template("admin/login.html", title="Admin Login")


# Logout
@app.route("/admin/logout/")
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))



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