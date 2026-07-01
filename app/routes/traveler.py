from flask import render_template
from app import app


@app.route("/")
def landing_page():
    return render_template("traveler/homePage.html", title="Home")


@app.route("/signup/")
def signup():
    return render_template("traveler/signUp.html", title="Sign Up")


@app.route("/login/")
def login():
    return render_template("traveler/login.html", title="Login")


@app.route("/otp/", methods=["GET","POST"])
def otp():
    return render_template("traveler/otp.html", title="OTP Verification")


@app.route("/dashboard/", methods=["GET", "POST"])
def dashboard():
    return render_template("traveler/dashboard.html", title="Dashboard")


@app.route("/explore/")
def destination():
    '''check out passing parameters through the url'''
    return render_template("traveler/dashboard_explore.html", title="Explore") # I think this should take a paramter of the actual "destination name" e.g. Chappal Waddi


@app.route("/guides/")
def guides():
    return render_template("traveler/guides.html", title="Guides") #attach actual dashboard-guides page

@app.route("/guide-details/")
def guide_details():
    return render_template("traveler/guide_details.html", title="Guide Details")


@app.route("/bookings/")
def bookings():     # I should be able to return a booking empty state here if the user has no bookings
    return render_template("traveler/bookings.html", title="Bookings") #attach actual dashboard-bookings page

# ===============================
# TEMP ROUTE FOR BOOKING EMPTY STATE (PLEASE DELETE LATER)
@app.route("/bes/")
def bed():
    return render_template("traveler/bookings_empty_state.html", title="Bookings") 
# ================================


@app.route("/profile/")
def profile():
    return render_template("traveler/profile.html", title="Profile") #attach actual dashboard-profile page


@app.route("/notifications/")
def notifications():
    return render_template("traveler/notifications.html", title="Notifications") #attach actual notification page


@app.route("/filter/")
def filter():
    return render_template("traveler/filter.html", title="Filter")


@app.route("/book-guide/")
def book_guide():
    return render_template("traveler/dashboard_bookGuide.html", title="Book a Guide")


@app.route("/booking-confirmation/")
def booking_confirmation():
    return render_template("traveler/booking_confirmation.html", title="Booking Confirmation")