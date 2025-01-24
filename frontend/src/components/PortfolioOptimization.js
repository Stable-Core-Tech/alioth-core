import React, { useState } from 'react';

function PortfolioOptimization() {
  const [portfolio, setPortfolio] = useState({});
  const [riskTolerance, setRiskTolerance] = useState(0.5);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/optimize-portfolio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portfolio, risk_tolerance: riskTolerance }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleAddToken = (e) => {
    e.preventDefault();
    const newPortfolio = { ...portfolio, '': 0 };
    setPortfolio(newPortfolio);
  };

  const handleTokenChange = (oldToken, newToken) => {
    const newPortfolio = { ...portfolio };
    delete newPortfolio[oldToken];
    newPortfolio[newToken] = 0;
    setPortfolio(newPortfolio);
  };

  const handleAmountChange = (token, amount) => {
    const newPortfolio = { ...portfolio, [token]: parseFloat(amount) };
    setPortfolio(newPortfolio);
  };

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-4">Portfolio Optimization</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        {Object.entries(portfolio).map(([token, amount], index) => (
          <div key={index} className="mb-2">
            <input
              type="text"
              value={token}
              onChange={(e) => handleTokenChange(token, e.target.value)}
              className="border rounded px-2 py-1 mr-2"
              placeholder="Token"
              required
            />
            <input
              type="number"
              value={amount}
              onChange={(e) => handleAmountChange(token, e.target.value)}
              className="border rounded px-2 py-1"
              placeholder="Amount"
              required
            />
          </div>
        ))}
        <button onClick={handleAddToken} className="bg-secondary text-white px-4 py-2 rounded mr-2">
          Add Token
        </button>
        <div className="mb-2">
          <label className="mr-2">Risk Tolerance (0-1):</label>
          <input
            type="number"
            value={riskTolerance}
            onChange={(e) => setRiskTolerance(parseFloat(e.target.value))}
            className="border rounded px-2 py-1"
            min="0"
            max="1"
            step="0.1"
            required
          />
        </div>
        <button type="submit" className="bg-primary text-white px-4 py-2 rounded">
          Optimize Portfolio
        </button>
      </form>
      {result && (
        <div>
          <h2 className="text-xl font-semibold mb-2">Optimized Portfolio:</h2>
          {Object.entries(result).map(([token, amount], index) => (
            <p key={index}>
              {token}: {amount.toFixed(2)}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export default PortfolioOptimization;

