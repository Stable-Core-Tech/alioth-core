import React, { useState } from 'react';

function RiskAssessment() {
  const [tokenData, setTokenData] = useState([]);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/risk-assessment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tokenData),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleAddPrice = (e) => {
    e.preventDefault();
    setTokenData([...tokenData, { price: 0 }]);
  };

  const handlePriceChange = (index, value) => {
    const newTokenData = [...tokenData];
    newTokenData[index].price = parseFloat(value);
    setTokenData(newTokenData);
  };

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-4">Risk Assessment</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        {tokenData.map((data, index) => (
          <div key={index} className="mb-2">
            <label className="mr-2">Price {index + 1}:</label>
            <input
              type="number"
              value={data.price}
              onChange={(e) => handlePriceChange(index, e.target.value)}
              className="border rounded px-2 py-1"
              required
            />
          </div>
        ))}
        <button onClick={handleAddPrice} className="bg-secondary text-white px-4 py-2 rounded mr-2">
          Add Price
        </button>
        <button type="submit" className="bg-primary text-white px-4 py-2 rounded">
          Assess Risk
        </button>
      </form>
      {result && (
        <div>
          <h2 className="text-xl font-semibold mb-2">Results:</h2>
          <p>Volatility: {result.volatility.toFixed(4)}</p>
          <p>Sharpe Ratio: {result.sharpe_ratio.toFixed(4)}</p>
          <p>Risk Score: {result.risk_score.toFixed(4)}</p>
        </div>
      )}
    </div>
  );
}

export default RiskAssessment;

