import React from 'react';
import EventCard from './EventCard';

function EventList({ events, joinEvent, deleteEvent }) {
  return (
    <div className="event-list">
      <h2>Available Events</h2>
      {events.length === 0 ? (
        <p>No events found.</p>
      ) : (
        events.map((event) => (
          <EventCard
            key={event.id}
            event={event}
            joinEvent={joinEvent}
            deleteEvent={deleteEvent}
          />
        ))
      )}
    </div>
  );
}

export default EventList;