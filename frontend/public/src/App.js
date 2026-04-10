import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import EventForm from './components/EventForm';
import EventList from './components/EventList';

const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [location, setLocation] = useState('');

  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${API_URL}/events`, {
        params: { search, category, location }
      });
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [search, category, location]);

  const addEvent = async (eventData) => {
    try {
      await axios.post(`${API_URL}/events`, eventData);
      fetchEvents();
    } catch (error) {
      console.error('Error adding event:', error);
    }
  };

  const joinEvent = async (id) => {
    try {
      await axios.put(`${API_URL}/events/${id}/join`);
      fetchEvents();
    } catch (error) {
      console.error('Error joining event:', error);
    }
  };

  const deleteEvent = async (id) => {
    try {
      await axios.delete(`${API_URL}/events/${id}`);
      fetchEvents();
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  return (
    <div>
      <Navbar />

      <div className="container">
        <div className="filters">
          <input
            type="text"
            placeholder="Search events..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <input
            type="text"
            placeholder="Filter by category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
          <input
            type="text"
            placeholder="Filter by location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>

        <EventForm addEvent={addEvent} />
        <EventList events={events} joinEvent={joinEvent} deleteEvent={deleteEvent} />
      </div>
    </div>
  );
}

export default App;