import os, secrets
from flask import render_template, request, url_for, flash, session, redirect
from app import app
from app.utils.auth_helpers import admin_required, check_admin_credentials
from app.models import db, Destination, destination_activities, Activity


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
            flash("Invalid credentials", category='danger')
            return render_template("admin/login.html", title="Admin Login")

    # GET request
    return render_template("admin/login.html", title="Admin Login")


# Logout 
@app.route("/admin/logout/")
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))


@app.route("/admin/analytics/")
@admin_required
def admin_analytics():
    return render_template("admin/analytics.html", title="Analytics")


@app.route("/admin/applications/")
@admin_required
def admin_applications():
    return render_template("admin/applications.html", title="Applications")


@app.route("/admin/guides/")
@admin_required
def admin_all_guides():
    return render_template("admin/all-guides.html", title="All Guides")


@app.route("/admin/destinations/", methods=['GET', 'POST'])
@admin_required
def admin_destinations():
    NIGERIAN_STATES = [
        "Abia",
        "Adamawa",
        "Akwa Ibom",
        "Anambra",
        "Bauchi",
        "Bayelsa",
        "Benue",
        "Borno",
        "Cross River",
        "Delta",
        "Ebonyi",
        "Edo",
        "Ekiti",
        "Enugu",
        "FCT",
        "Gombe",
        "Imo",
        "Jigawa",
        "Kaduna",
        "Kano",
        "Katsina",
        "Kebbi",
        "Kogi",
        "Kwara",
        "Lagos",
        "Nasarawa",
        "Niger",
        "Ogun",
        "Ondo",
        "Osun",
        "Oyo",
        "Plateau",
        "Rivers",
        "Sokoto",
        "Taraba",
        "Yobe",
        "Zamfara"
    ]

   
    if request.method == 'POST':

        #1 Getting activity types from the form
        activity_string = request.form.get("activity_types", "")
        activities = activity_string.split(",")

        #2 Saving New Destination
        destination_name = request.form.get('destination_name')
        state = request.form.get('state')
        difficulty = request.form.get('difficulty')
        desc = request.form.get('description')
        safety_notes = request.form.get('safety_notes')

        # Image
        filename = None
        image = request.files.get('destination_image')
        if image:
            name, ext = os.path.splitext(image.filename)
            generated_img_filename = secrets.token_hex(32)
            filename = f'{generated_img_filename}{ext}'
            upload_path = f'app/static/uploads/{filename}'
            image.save(upload_path)


        # Inserting into Database
        new_dest = Destination(
            name=destination_name,
            state=state,
            description=desc,
            difficulty_level=difficulty,
            safety_notes=safety_notes,
            image_path=filename
        )
        db.session.add(new_dest)
        db.session.commit()

        # 3. Looping through every activity submitted with the form
        for activity_name in activities:
            activity_name = activity_name.strip().title()
            
            if not activity_name:
                continue

            activity = Activity.query.filter_by(name=activity_name).first()

            if activity is None:
                activity = Activity(name=activity_name, icon=None)
                db.session.add(activity)

            new_dest.activity_tags.append(activity)

        # This saves the "relationships" to the db
        db.session.commit()

        flash("Destination added successfully!", "success")
        return redirect(url_for("admin_destinations"))

    # Get request
    return render_template("admin/destinations.html", title="Destinations", states=NIGERIAN_STATES)


@app.route("/admin/bookings/")
@admin_required
def admin_all_bookings():
    return render_template("admin/all-bookings.html", title="All Bookings")


@app.route("/admin/reviews/")
@admin_required
def admin_reviews():
    return render_template("admin/reviews.html", title="Reviews")