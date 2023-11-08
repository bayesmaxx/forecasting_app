import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import ForecastPage from './pages/ForecastPage';
import AboutPage from './pages/AboutPage';
import SpecificForecast from './pages/SpecificForecast'
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Switch>
          <Route exact path="/" component={ForecastPage}/>
          <Route path="/:id" component={SpecificForecast}/>
          <Route exact path="/about" component={AboutPage}/>
        </Switch>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
