import React from 'react';
import { Link, useParams } from 'react-router-dom';
import '../styles/Instructions.css'; // Assicurati di importare il file CSS per lo stile

const Instructions = () => {
  const { index } = useParams();
  

  return (
    <div className="instructions-container">
      <h1>Instructions</h1>
      <p>Welcome to the instructions page!</p>
      {index && (
        <Link to={`/exercitropo/${index}`}>
          <button className="start-button">Start</button>
        </Link>
      )}
    </div>
  );
};

export default Instructions;
