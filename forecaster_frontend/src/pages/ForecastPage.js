import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';


function ForecastPage() {
    const [forecasts, setForecasts] = useState([]);
  
    useEffect(() => {
      // Fetch the list of forecasts from your API
      fetch('http://127.0.0.1:8000/forecaster/api/forecasts/')
        .then(response => response.json())
        .then(data => setForecasts(data))
        .catch(error => console.error('Error fetching data: ', error));
    }, []);
  
    return (
      <div>
        <h1>Forecasts</h1>
        <ul>
          {forecasts.map((forecast) => (
            <li key={forecast.id}>
              <Link to={`/forecasts/${forecast.id}`}>
                {forecast.title}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    );
  }
  
  export default ForecastPage;
