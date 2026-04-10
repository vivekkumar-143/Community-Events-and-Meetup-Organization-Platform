from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Event

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'message': 'Community Events API is running'})

@app.route('/events', methods=['GET'])
def get_events():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    location = request.args.get('location', '')

    events = Event.query.all()
    result = []

    for event in events:
        event_data = event.to_dict()

        if search and search.lower() not in event.title.lower() and search.lower() not in event.description.lower():
            continue
        if category and category.lower() != event.category.lower():
            continue
        if location and location.lower() not in event.location.lower():
            continue

        result.append(event_data)

    return jsonify(result)

@app.route('/events', methods=['POST'])
def add_event():
    data = request.json

    new_event = Event(
        title=data['title'],
        category=data['category'],
        location=data['location'],
        date=data['date'],
        time=data['time'],
        description=data['description'],
        organizer=data['organizer'],
        participants=0
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event created successfully', 'event': new_event.to_dict()}), 201

@app.route('/events/<int:event_id>/join', methods=['PUT'])
def join_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({'message': 'Event not found'}), 404

    event.participants += 1
    db.session.commit()

    return jsonify({'message': 'Joined event successfully', 'event': event.to_dict()})

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({'message': 'Event not found'}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({'message': 'Event deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)