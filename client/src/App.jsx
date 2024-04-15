import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState('');
  const [breed, setBreed] = useState('');
  const [confidence, setConfidence] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('http://localhost:9000/history');
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:9000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.status === 200) {
        setBreed(`Predicted Breed: ${response.data.breed_name}`);
        setConfidence(`Confidence: ${response.data.confidence}`);
        setError('');
        fetchHistory();  // Refresh history after a new prediction
      } else {
        setError('Failed to get a valid response from the server');
        setBreed('');
        setConfidence('');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to connect to the API');
      setBreed('');
      setConfidence('');
    }
    setIsLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Dog Breed Classifier</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" className="custom-file-input" onChange={handleFileChange} />
          {imagePreviewUrl && <img src={imagePreviewUrl} alt="Dog Preview" />}
          <button type="submit">Classify Breed</button>
        </form>
        {isLoading && <p>Loading...</p>}
        {breed && <p>{breed}</p>}
        {confidence && <p>{confidence}</p>}
        {error && <p className="error">{error}</p>}
        <h2>Prediction History</h2>
        <div>
          {history.map((entry, index) => (
            <div key={index}>
              <p>{entry.timestamp}: {entry.breed_name} - Confidence: {entry.confidence}%</p>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
