import React, { useState, useEffect, useCallback } from 'react';
import '../styles/ExerciTropo.css';

const ExerciTropo = () => {
  const [index, setIndex] = useState(0);
  const [chatMessages, setChatMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);

  const initializeChat = useCallback(() => {
    setChatMessages([
      {
        type: 'bot',
        message: "Piacere io sono un trainer metaforico. Il gioco consiste di vari livelli. In questa prima fase dovrai semplicemente descrivere le immagini, dettagliando cosa vedi, elencando le varie caratteristiche dei soggetti rappresentati... Io per adesso non esprimerò alcun giudizio, confermandoti se hai fatto bene o no.",
      },
    ]);
  }, []);

  const fetchBotResponse = useCallback(async (message) => {
    setLoading(true);
    try {
      const response = await fetch('/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, index }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setChatMessages(prevMessages => [
        ...prevMessages,
        { type: 'bot', message: data.message },
      ]);
    } catch (error) {
      console.error('Error fetching bot response:', error);
      setChatMessages(prevMessages => [
        ...prevMessages,
        { type: 'bot', message: "Sorry, there was an error processing your request." },
      ]);
    } finally {
      setLoading(false);
    }
  }, [index]);

  const handleImageChange = async (newIndex) => {
    setIndex(newIndex);
    setChatMessages([]);

    try {
      const endpoint = newIndex >= index ? `/set_image?msg=${newIndex}` : `/set_again_image?msg=${newIndex}`;
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      await response.text();

      setChatMessages(prevMessages => [
        ...prevMessages,
        {
          type: 'bot',
          message: "In questa fase dovrai semplicemente descrivere le immagini, dettagliando cosa vedi, elencando le varie caratteristiche dei soggetti rappresentati... Io per adesso non esprimerò alcun giudizio, confermandoti se hai fatto bene o no.",
        },
      ]);
    } catch (error) {
      console.error('Error changing image:', error);
      setChatMessages(prevMessages => [
        ...prevMessages,
        { type: 'bot', message: "Sorry, there was an error processing your request." },
      ]);
    }
  };

  const nextImage = () => {
    handleImageChange(index + 1);
  };

  const goBackImage = () => {
    if (index > 0) {
      handleImageChange(index - 1);
    }
  };

  const getBotResponse = async () => {
    const rawText = userInput.trim();
    if (!rawText) return;

    setChatMessages(prevMessages => [...prevMessages, { type: 'user', message: rawText }]);
    setUserInput(''); // Svuota il campo di input

    try {
      await fetchBotResponse(rawText);
    } catch (error) {
      console.error('Error processing bot response:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      getBotResponse();
    }
  };

  useEffect(() => {
    initializeChat();
  }, [initializeChat]);

  return (
    <div>
      <h1 className="title">L'ExerciTropo</h1>
      <h4 className="subtitle">Questo è un training metaforico</h4>
      <div className="button-container">
        <button className="bottone" onClick={goBackImage} disabled={index === 0}>Indietro</button>
        <button className="bottone" onClick={nextImage}>Avanti</button>
      </div>
      <div className="image-container">
        <img
          id="myImage"
          src={`/images/${index}.png`} // Percorso relativo alla cartella public
          alt={`immagine ${index}`}
        />
      </div>
      <div className="boxed">
        <div id="chatbox" aria-live="polite">
          {chatMessages.map((msg, idx) => (
            <p key={idx} className={msg.type === 'bot' ? 'botText' : 'userText'}>
              <span>{msg.message}</span>
            </p>
          ))}
        </div>
        <div id="userInput">
          <input
            id="textInput"
            type="text"
            name="msg"
            placeholder="Message"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={handleKeyPress}
            autoComplete="off" // Disabilita l'autocompletamento del browser
          />
        </div>
        {loading && <img id="loadingGif" src="/images/loading-4802_128.gif" alt="Loading..." />}
      </div>
    </div>
  );
};

export default ExerciTropo;
