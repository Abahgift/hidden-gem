import random
from datetime import datetime, timedelta
from flask import request, session, redirect, url_for, flash, render_template
from flask_mailman import EmailMessage

from app import app
from app.models import db, User

OTP_VALIDITY_MINUTES = 10


def send_otp_email(email):
    """Generates, stores in database and session, and emails a fresh OTP. Callable directly
    from signup() in traveler.py / guide.py — no redirect needed."""
    otp_code = f"{random.randint(100000, 999999)}"
    
    # Store email context in session
    session['otp_email'] = email
    
    # Save the OTP details to the user record in database
    user = User.query.filter_by(email=email).first()
    if user:
        user.otp_code = otp_code
        user.otp_expires_at = datetime.utcnow() + timedelta(minutes=OTP_VALIDITY_MINUTES)
        db.session.commit()
    else:
        raise ValueError(f"No user found with email address: {email}")

    msg = EmailMessage(
        subject="Your Hidden Gems Verification Code",
        body=f"Your verification code is: {otp_code}. It expires in {OTP_VALIDITY_MINUTES} minutes.",
        to=[email],
    )
    msg.send()


@app.route('/request-otp/', methods=['POST'])
def request_otp():
    """Resend endpoint only — reuses the email already sitting in session
    from signup, so no form field is needed."""
    email = session.get('otp_email')
    if not email:
        flash("Your session expired. Please sign up again.", category="errormsg")
        return redirect(url_for('signup'))

    try:
        send_otp_email(email)
        flash("A new code has been sent.")
    except Exception as e:
        flash(f"Couldn't send verification email: {str(e)}", category="errormsg")

    return redirect(url_for('verify_otp_page'))


@app.route('/verify-otp-page/', methods=['GET', 'POST'])
def verify_otp_page():
    email = session.get('otp_email')
    if not email:
        return redirect(url_for('signup'))

    if request.method == 'POST':
        user_input = request.form.get('otp')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User not found. Please sign up again.", category="errormsg")
            return redirect(url_for('signup'))

        stored_otp = user.otp_code
        expires_at = user.otp_expires_at

        # Check expiration
        if not stored_otp or not expires_at or datetime.utcnow() > expires_at:
            user.otp_code = None
            user.otp_expires_at = None
            db.session.commit()
            
            session.pop('otp_email', None)
            flash("Your code has expired. Please request a new one.", category="errormsg")
            return redirect(url_for('signup'))

        # Check matching OTP
        if user_input == stored_otp:
            user.is_verified = True
            user.otp_code = None
            user.otp_expires_at = None
            db.session.commit()

            # Clean session helper
            session.pop('otp_email', None)
            
            # Log the user in
            session['user_id'] = user.id
            session['user_role'] = user.role

            if user.role == 'traveler':
                flash("Email verified successfully! Welcome to Hidden Gems.")
                return redirect(url_for('dashboard'))
            else:
                flash("Email verified successfully! Welcome to Hidden Gems.")
                return redirect(url_for('guide_dashboard'))
        else:
            flash("Invalid code. Please try again.", category="errormsg")
        
    return render_template('traveler/otp.html')
