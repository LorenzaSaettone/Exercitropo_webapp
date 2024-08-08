import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';// Importa il file CSS per lo stile

const Home = () => {
  const [inputString, setInputString] = useState('');
  const [inputIndex, setInputIndex] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/login', { inputString, inputIndex });
      console.log(response.data); // Debugging line

      if (response.data.authenticated) {
        setError('');
        navigate(`/instructions/${inputIndex}`);
      } else {
        setError('Login Errato: controlla le tue credenziali o di aver inserito il numero corretto del trial.');
      }
    } catch (error) {
      console.error('Error logging in:', error);
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div className="home-container">
      <h1 className="home-title">Login</h1>
      <form className="home-form" onSubmit={handleLogin}>
        <input
          type="text"
          className="home-input"
          value={inputString}
          onChange={(e) => setInputString(e.target.value)}
          placeholder="Enter your password"
          required
        />
        <input
          type="text"
          className="home-input"
          value={inputIndex}
          onChange={(e) => setInputIndex(e.target.value)}
          placeholder="Enter your index"
          required
        />
        <button type="submit" className="home-button">Login</button>
      </form>
      {error && <p className="home-error">{error}</p>}
    </div>
  );
};

export default Home;
