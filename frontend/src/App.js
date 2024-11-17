// src/App.js
import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import './App.css';

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = io('http://127.0.0.1:5000');

    // Listen for 'update' event from the backend
    socket.on('update', (newItems) => {
      setItems(newItems); // Update state with the received items
    });

    // Cleanup WebSocket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []); // Empty dependency array ensures this effect runs once (componentDidMount)

  return (
    <div className="App">
      <h1>Items List</h1>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - £{item.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
