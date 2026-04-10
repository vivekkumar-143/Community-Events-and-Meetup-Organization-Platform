import React from 'react';

function EventCard({ event, joinEvent, deleteEvent }) {
  return (
    <div className="event-card">
      <h3>{event.title}</h3>
      <p><strong>Category:</strong> {event.category}</p>
      <p><strong>Location:</strong> {event.location}</p>
      <p><strong>Date:</strong> {event.date}</p>
      <p><strong>Time:</strong> {event.time}</p>
      <p><strong>Organizer:</strong> {event.organizer}</p>
      <p><strong>Description:</strong> {event.description}</p>
      <p><strong>Participants:</strong> {event.participants}</p>
      <div className="card-buttons">
        <button onClick={() => joinEvent(event.id)}>Join</button>
        <button className="delete-btn" onClick={() => deleteEvent(event.id)}>Delete</button>
      </div>
    </div>
  );
}

export default EventCard;