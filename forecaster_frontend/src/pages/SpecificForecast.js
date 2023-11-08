import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function SpecificForecast() {
    const [forecastDetail, setForecastDetail] = useState(null);
    const [relatedData, setRelatedData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    let { id } = useParams();
  
    useEffect(() => {
      Promise.all([
        fetch(`http://127.0.0.1:8000/forecaster/api/forecasts/${id}/`),
        fetch(`http://127.0.0.1:8000/forecaster/api/forecast_points/?forecast=${id}/`)
      ])
      .then(async ([res1, res2]) => {
        if (!res1.ok || !res2.ok) {
          throw new Error('Error fetching data');
        }
        const data1 = await res1.json();
        const data2 = await res2.json();
        return [data1, data2];
      })
      .then(([data1, data2]) => {
        setForecastDetail(data1);
        setRelatedData(data2);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
    }, [id]);
  
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error loading the forecast: {error.message}</div>;
    if (!forecast) return <div>Forecast not found</div>;

    return (
        <div>
        <h1>{forecast.title}</h1>
        {/* Display other details of the forecast */}
        </div>
    );
}

export default ForecastDetail;