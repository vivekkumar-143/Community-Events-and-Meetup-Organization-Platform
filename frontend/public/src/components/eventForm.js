import React, { useState } from 'react';

function EventForm({ addEvent }) {
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    location: '',
    date: '',
    time: '',
    description: '',
    organizer: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addEvent(formData);
    setFormData({
      title: '',
      category: '',
      location: '',
      date: '',
      time: '',
      description: '',
      organizer: ''
    });
  };

  return (
    <form className="event-form" onSubmit={handleSubmit}>
      <h2>Create New Event</h2>
      <input type="text" name="title" placeholder="Event Title" value={formData.title} onChange={handleChange} required />
      <input type="text" name="category" placeholder="Category" value={formData.category} onChange={handleChange} required />
      <input type="text" name="location" placeholder="Location" value={formData.location} onChange={handleChange} required />
      <input type="date" name="date" value={formData.date} onChange={handleChange} required />
      <input type="time" name="time" value={formData.time} onChange={handleChange} required />
      <textarea name="description" placeholder="Description" value={formData.description} onChange={handleChange} required></textarea>
      <input type="text" name="organizer" placeholder="Organizer Name" value={formData.organizer} onChange={handleChange} required />
      <button type="submit">Create Event</button>
    </form>
  );
}

export default EventForm;