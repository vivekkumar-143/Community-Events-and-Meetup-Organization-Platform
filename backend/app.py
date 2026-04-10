from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Event
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()


def send_email(receiver_email, subject, body):
    if not receiver_email:
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = app.config["SMTP_EMAIL"]
        msg["To"] = receiver_email
        msg.set_content(body)

        server = smtplib.SMTP(app.config["SMTP_SERVER"], app.config["SMTP_PORT"])
        server.starttls()
        server.login(app.config["SMTP_EMAIL"], app.config["SMTP_PASSWORD"])
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email error:", e)


@app.route("/")
def home():
    return jsonify({"message": "MeetSphere API is running successfully"})


@app.route("/stats", methods=["GET"])
def stats():
    total_events = Event.query.count()
    total_users = User.query.count()
    total_organizers = User.query.filter_by(role="Organizer").count()
    total_participants = User.query.filter_by(role="Participant").count()

    return jsonify({
        "total_events": total_events,
        "total_users": total_users,
        "total_organizers": total_organizers,
        "total_participants": total_participants
    })


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    full_name = data.get("full_name", "").strip()
    role = data.get("role", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not full_name or not role or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(
        full_name=full_name,
        role=role,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    send_email(
        email,
        "Welcome to MeetSphere",
        f"Hello {full_name},\n\nYour account has been created successfully as a {role}.\n\nWelcome to MeetSphere!"
    )

    return jsonify({
        "message": "Account created successfully",
        "user": new_user.to_dict()
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200


@app.route("/events", methods=["GET"])
def get_events():
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    location = request.args.get("location", "").strip().lower()
    featured = request.args.get("featured", "").strip().lower()

    events = Event.query.order_by(Event.id.desc()).all()
    result = []

    for event in events:
        if search and search not in event.title.lower() and search not in event.description.lower():
            continue
        if category and category != event.category.lower():
            continue
        if location and location not in event.location.lower():
            continue
        if featured == "true" and not event.featured:
            continue

        result.append(event.to_dict())

    return jsonify(result)


@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json()

    required_fields = ["title", "category", "location", "date", "time", "description", "organizer"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    new_event = Event(
        title=data["title"],
        category=data["category"],
        location=data["location"],
        date=data["date"],
        time=data["time"],
        description=data["description"],
        organizer=data["organizer"],
        organizer_email=data.get("organizer_email", ""),
        participants=0,
        featured=bool(data.get("featured", False))
    )

    db.session.add(new_event)
    db.session.commit()

    if new_event.organizer_email:
        send_email(
            new_event.organizer_email,
            "Your Event Has Been Created",
            f"Hello {new_event.organizer},\n\nYour event '{new_event.title}' has been created successfully.\nDate: {new_event.date}\nTime: {new_event.time}\nLocation: {new_event.location}"
        )

    return jsonify({
        "message": "Event created successfully",
        "event": new_event.to_dict()
    }), 201


@app.route("/events/<int:event_id>/join", methods=["PUT"])
def join_event(event_id):
    data = request.get_json(silent=True) or {}

    user_email = data.get("email", "").strip().lower()
    user_name = data.get("full_name", "").strip()

    event = Event.query.get(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    event.participants += 1
    db.session.commit()

    if user_email:
        send_email(
            user_email,
            "Event Join Confirmation",
            f"Hello {user_name or 'User'},\n\nYou have successfully joined '{event.title}'.\nDate: {event.date}\nTime: {event.time}\nLocation: {event.location}\nOrganizer: {event.organizer}"
        )

    if event.organizer_email:
        send_email(
            event.organizer_email,
            "A Participant Joined Your Event",
            f"Hello {event.organizer},\n\nA new participant joined your event '{event.title}'."
        )

    return jsonify({
        "message": "Joined event successfully",
        "event": event.to_dict()
    })


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
    # updated for new commit