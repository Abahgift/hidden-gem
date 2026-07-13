"""
Hidden Gems — SQLAlchemy Models (Flask-SQLAlchemy + Flask-Migrate)
--------------------------------------------------------------------
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ─────────────────────────────────────────────────────────────
#  ASSOCIATION / JUNCTION TABLES  (pure many-to-many, no extra data)
# ─────────────────────────────────────────────────────────────

guide_languages = db.Table(
    "guide_languages",
    db.Column("guide_id", db.Integer, db.ForeignKey("tour_guides.id"), primary_key=True),
    db.Column("language_id", db.Integer, db.ForeignKey("languages.id"), primary_key=True),
)

guide_activities = db.Table(
    "guide_activities",
    db.Column("guide_id", db.Integer, db.ForeignKey("tour_guides.id"), primary_key=True),
    db.Column("activity_id", db.Integer, db.ForeignKey("activities.id"), primary_key=True),
)

destination_activities = db.Table(
    "destination_activities",
    db.Column("destination_id", db.Integer, db.ForeignKey("destinations.id"), primary_key=True),
    db.Column("activity_id", db.Integer, db.ForeignKey("activities.id"), primary_key=True),
)

guide_destinations = db.Table(
    "guide_destinations",
    db.Column("guide_id", db.Integer, db.ForeignKey("tour_guides.id"), primary_key=True),
    db.Column("destination_id", db.Integer, db.ForeignKey("destinations.id"), primary_key=True),
)


# ─────────────────────────────────────────────────────────────
#  USERS
# ─────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    state_of_residence = db.Column(db.String(100), nullable=True)


    role = db.Column(
        db.Enum("traveler", "guide", "admin", name="user_role"),
        nullable=False,
        default="traveler",
    )

    # Email verification
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expires_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    guide_profile = db.relationship(
        "TourGuide", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    bookings_made = db.relationship(
        "Booking", back_populates="traveler", foreign_keys="Booking.traveler_id"
    )
    reviews_written = db.relationship("Review", back_populates="reviewer")

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.id} {self.email} ({self.role})>"


# ─────────────────────────────────────────────────────────────
#  LOOKUP TABLES: LANGUAGES + ACTIVITIES
# ─────────────────────────────────────────────────────────────

class Language(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    guides = db.relationship(
        "TourGuide", secondary=guide_languages, back_populates="languages"
    )

    def __repr__(self):
        return f"<Language {self.name}>"


class Activity(db.Model):
    """
    Shared lookup table for activity/expertise tags — used both as a guide's
    area of expertise (e.g. Hiking, Camping) and as a destination's activity
    tags (e.g. Trekking, Wildlife). Keeping this as one table avoids two
    near-identical enums drifting out of sync.
    """
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    icon = db.Column(db.String(10), nullable=True)  # optional emoji, e.g. "🥾"

    guides = db.relationship(
        "TourGuide", secondary=guide_activities, back_populates="expertise"
    )
    destinations = db.relationship(
        "Destination", secondary=destination_activities, back_populates="activity_tags"
    )

    def __repr__(self):
        return f"<Activity {self.name}>"


# ─────────────────────────────────────────────────────────────
#  TOUR GUIDES
# ─────────────────────────────────────────────────────────────

class TourGuide(db.Model):
    __tablename__ = "tour_guides"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    bio = db.Column(db.Text, nullable=True)
    price_per_day = db.Column(db.Integer, nullable=True)  # NGN, whole numbers
    years_experience = db.Column(db.Integer, nullable=True)
    max_group_size = db.Column(db.Integer, nullable=True)
    operating_state = db.Column(db.String(60), nullable=True)  # e.g. "Taraba"

    is_available = db.Column(db.Boolean, default=True)
    verification_status = db.Column(
        db.Enum("pending", "verified", "rejected", name="guide_verification_status"),
        nullable=False,
        default="pending",
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    user = db.relationship("User", back_populates="guide_profile")
    languages = db.relationship(
        "Language", secondary=guide_languages, back_populates="guides"
    )
    expertise = db.relationship(
        "Activity", secondary=guide_activities, back_populates="guides"
    )
    destinations_covered = db.relationship(
        "Destination", secondary=guide_destinations, back_populates="guides"
    )
    bookings = db.relationship("Booking", back_populates="guide")

    def __repr__(self):
        return f"<TourGuide {self.id} user={self.user_id}>"


# ─────────────────────────────────────────────────────────────
#  DESTINATIONS
# ─────────────────────────────────────────────────────────────

class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=True)
    description = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(
        db.Enum("Easy", "Moderate", "Hard", "Extreme", name="difficulty_level"),
        nullable=False,
        default="Easy",
    )
    safety_notes = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(10), nullable=True)  # emoji shown on cards

    created_by_admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    created_by = db.relationship("User", foreign_keys=[created_by_admin_id])
    activity_tags = db.relationship(
        "Activity", secondary=destination_activities, back_populates="destinations"
    )
    guides = db.relationship(
        "TourGuide", secondary=guide_destinations, back_populates="destinations_covered"
    )
    images = db.relationship(
        "DestinationImage", back_populates="destination", cascade="all, delete-orphan"
    )
    bookings = db.relationship("Booking", back_populates="destination")

    def __repr__(self):
        return f"<Destination {self.name}>"


class DestinationImage(db.Model):
    __tablename__ = "destination_images"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)
    image_name = db.Column(db.String(120), nullable=True)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    destination = db.relationship("Destination", back_populates="images")

    def __repr__(self):
        return f"<DestinationImage {self.id} for dest={self.destination_id}>"


# ─────────────────────────────────────────────────────────────
#  BOOKINGS
# ─────────────────────────────────────────────────────────────

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    traveler_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey("tour_guides.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)

    trip_date = db.Column(db.Date, nullable=False)
    duration_days = db.Column(db.Integer, default=1)
    party_size = db.Column(db.Integer, default=1)
    amount = db.Column(db.Numeric(10, 2), nullable=True)  # quoted price, NOT a payment record

    status = db.Column(
        db.Enum("pending", "confirmed", "completed", "cancelled", name="booking_status"),
        nullable=False,
        default="pending",
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    traveler = db.relationship("User", back_populates="bookings_made", foreign_keys=[traveler_id])
    guide = db.relationship("TourGuide", back_populates="bookings")
    destination = db.relationship("Destination", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.id} status={self.status}>"


# ─────────────────────────────────────────────────────────────
#  REVIEWS
# ─────────────────────────────────────────────────────────────

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Polymorphic target: either a destination or a guide.
    # (No DB-level FK constraint possible on target_id since it can point to
    # two different tables — this is enforced in application/service logic.)
    target_type = db.Column(
        db.Enum("destination", "guide", name="review_target_type"), nullable=False
    )
    target_id = db.Column(db.Integer, nullable=False)

    rating = db.Column(db.Numeric(2, 1), nullable=False)  # e.g. 4.5
    comment = db.Column(db.Text, nullable=True)
    guide_reply = db.Column(db.Text, nullable=True)  # guide's response to the review

    moderation_status = db.Column(
        db.Enum("pending", "approved", "flagged", name="review_moderation_status"),
        nullable=False,
        default="approved",
    )
    flag_reason = db.Column(db.String(150), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    reviewer = db.relationship("User", back_populates="reviews_written")

    def __repr__(self):
        return f"<Review {self.id} target={self.target_type}:{self.target_id}>"