import React from 'react';
import ReactDOM from 'react-dom/client'; // Import the new ReactDOM API
import App from './App';
import './index.css'; // You can add styles here

// Create a root to render your app
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
