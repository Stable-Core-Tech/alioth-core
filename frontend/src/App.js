import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import RiskAssessment from './components/RiskAssessment';
import TradingAgent from './components/TradingAgent';
import PortfolioOptimization from './components/PortfolioOptimization';
import './styles.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route path="/risk-assessment" component={RiskAssessment} />
          <Route path="/trading-agent" component={TradingAgent} />
          <Route path="/portfolio-optimization" component={PortfolioOptimization} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;

