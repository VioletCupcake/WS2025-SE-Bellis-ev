// src/services/api.js
import axios from 'axios';

// Create a reusable axios instance
export const api = axios.create({
  baseURL: 'http://localhost:8000/api', // <-- replace with your backend URL
  headers: {
    'Content-Type': 'application/json',
  }
});

// Example helper functions (optional)
export const getFalls = () => api.get('/falls');
export const createFall = (data) => api.post('/falls', data);
