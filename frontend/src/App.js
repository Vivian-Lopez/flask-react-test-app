// src/App.js
import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  
  // Called when the App component mounts
  // what is a mount? Inserting a component into the DOM
  useEffect(() => {
    // Connect to the WebSocket server - using their ip and port
    const socket = io('http://127.0.0.1:5000');

    // Listen for 'update' event from the backend
    // socket automatically parses the json so we don't need to explicitly parse it
    // This is essentially the handler for the update event which is sent by emit on the backend
    // It updates the items state, causing the component to re-render which is what we want
    socket.on('update', (newItems) => {
      setItems(newItems); // Update state with the received items
    });

    // Cleanup WebSocket connection when the component unmounts
    // avoiding memory leaks and unwanted connections still being open when
    // this component is removed from the DOM
    // What is DOM? Document Object model
    // represents the structure of a webpage as a tree of objects
    // every element in an HTML document becomes a node in this tree.
    // DOM allows JS or React to interact, modify and manipulate the structure of the webpage
    // dynamically
    // With React, Virtual DOM is used which is a lightweight copy of the DOM.
    // React updates the part of the DOM that changes, instead of re-rendering the entire DOM tree
    // React finds the diff and also batches updates from the virtual DOM, reducing re-renders
    // reduces reflows (layout recalculations) and repaints (redrawing elements) as a result of fewer re-renders
    // Also virtual DOM is in memory so it is faster to manipulate.
    // Lets developers focus on UI while React hanldes efficient updates.
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
