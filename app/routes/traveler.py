from unicodedata import category

from datetime import datetime
from flask import render_template, request, url_for, redirect,session,flash
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, User
from app.routes.auth import send_otp_email


@app.route("/")
def landing_page():
    return render_template("traveler/homePage.html", title="Home")


@app.route("/signup/", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get("confirm_password")
        userrole = request.form.get('user_role') 
        verification = False

        # Validation
        if firstname and lastname and email and password:
            # Uniqueness check
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email address already registered. Please log in.", category="errormsg")
                return redirect(url_for('signup'))

            if password == confirmpassword:
                hash = generate_password_hash(password)
                user = User(first_name=firstname, last_name=lastname, email=email,
                            password_hash=hash, role=userrole, is_verified=False)
                db.session.add(user)
                db.session.commit()

                try:
                    send_otp_email(email)
                except Exception as e:
                    flash(f"Account created, but we couldn't send your verification code: {str(e)}", category="errormsg")

                return redirect(url_for('verify_otp_page'))
            else:
                flash("Both passwords must match", category="errormsg")
                return redirect(url_for('signup'))
        else:
            flash("All fields are required", category='errormsg')
            return redirect(url_for('signup'))

    return render_template("traveler/signUp.html", title="Sign Up")



@app.route("/login/", methods=['GET',"POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter(User.email==email).first()

        if user:
            stored_password = user.password_hash
            check = check_password_hash(stored_password, password)

            if check:
                session['useronline'] = user.id
                if user.role == 'traveler':
                    session['traveleronline'] = user.id
                    return redirect(url_for('dashboard'))
                
                if user.role == 'guide':
                    session['guideonline'] = user.id
                    return redirect(url_for('guide_dashboard'))
                
            else:
                flash("Password is incorrect. Please check again", category="errormsg")

                return redirect(url_for("login"))
        else:
            flash("Email not found. Please register an account", category="errormsg")
            return redirect(url_for("login"))
 
    return render_template("traveler/login.html", title="Login")


@app.route("/dashboard/", methods=["GET", "POST"])
def dashboard():
    if session.get("useronline") is None:
        flash("You must be logged in to access your dashboard",category="errormsg")
        return redirect(url_for("login"))
    
    user = User.query.get(session.get("useronline"))
    return render_template("traveler/dashboard.html", title="Dashboard", user=user)


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
    return render_template("traveler/bookings_upcoming.html", title="Bookings") #attach actual dashboard-bookings page

# ===============================
# TEMP ROUTE FOR BOOKING EMPTY STATE (PLEASE DELETE LATER)
@app.route("/bes/")
def bed():
    return render_template("traveler/bookings_empty_state.html", title="Bookings") 
# ================================

@app.route("/bookings/past/")
def past_bookings():  # New route for past bookings
    return render_template("traveler/bookings_past.html", title="Past Bookings")


@app.route("/bookings/cancelled/")
def cancelled_bookings():  # New route for past bookings
    return render_template("traveler/bookings_cancelled.html", title="Cancelled Bookings")


# ===============================
# PROFILE STARTS HERE
@app.route("/profile/<int:id>/", methods=['GET', 'POST'])
def profile(id):
    if session.get("useronline") is None:
        flash("You must be logged in to access your profile", category="errormsg")
        return redirect(url_for("login"))

    # Prevents a user from accidentally editing another different user's profile
    user = User.query.get(session.get("useronline"))
    if user.id != id:
        flash("You are not the owner of that profile", category="danger")
        return redirect(url_for('dashboard'))

    if request.method == "POST":

        form_type = request.form.get('form_type')

        if form_type == 'profile':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone = request.form.get('phone')
            state = request.form.get('state')

            if not firstname or not lastname:
                flash('First and last name cannot be empty.', category='danger')
            else:
                user.first_name = firstname
                user.last_name = lastname
                user.phone_number = phone
                user.state_of_residence = state
                db.session.commit()
                flash('Profile Updated Successfully!', category='success')

            return redirect(url_for('profile', id=id))
        
        elif form_type == 'password':
            current_pwd = request.form.get('password')
            new_pwd = request.form.get('newpassword')
            confirm_pwd = request.form.get('confirmpassword')

            if not check_password_hash(user.password_hash, current_pwd):
                flash('Current password is incorrect. Try again', category='danger')

            elif new_pwd != confirm_pwd:
                flash('New password and confirm password do not match.', category='danger')
            else:
                user.password_hash = generate_password_hash(new_pwd)
                db.session.commit()
                flash('Password updated successfully.', category='success')
            return redirect(url_for('profile', id=id))
        
        else:
            flash('Invalid form submission.', category='danger')
            return redirect(url_for('profile', id=id))
        

    # GET request
    return render_template("traveler/profile.html", title="Profile", user=user)



@app.route("/profile/saved-destinations/")
def saved_destinations():
    return render_template("traveler/profile_saved_destinations.html", title="Saved Destinations")


@app.route("/profile/preference/")
def preference():
    return render_template("traveler/profile_preference.html", title="Preference")


@app.route("/profile/recent-activity/")
def recent_activity():
    return render_template("traveler/profile_recent_activity.html", title="Recent Activity")

# PROFILE ENDS HERE
# ===============================


@app.route("/notifications/")
def notifications():
    return render_template("traveler/notification.html", title="Notifications") #attach actual notification page


@app.route("/filter/")
def filter():
    return render_template("traveler/filter.html", title="Filter")


@app.route("/book-guide/")
def book_guide():
    return render_template("traveler/dashboard_bookGuide.html", title="Book a Guide")


@app.route("/booking-confirmation/")
def booking_confirmation():
    return render_template("traveler/booking_confirmation.html", title="Booking Confirmation")
