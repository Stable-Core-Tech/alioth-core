import React, { useState } from 'react';

function TradingAgent() {
  const [token, setToken] = useState('');
  const [amount, setAmount] = useState('');
  const [action, setAction] = useState('buy');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/execute-trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, amount: parseFloat(amount), action }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-4">Trading Agent</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="mb-2">
          <label className="mr-2">Token:</label>
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            className="border rounded px-2 py-1"
            required
          />
        </div>
        <div className="mb-2">
          <label className="mr-2">Amount:</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="border rounded px-2 py-1"
            required
          />
        </div>
        <div className="mb-2">
          <label className="mr-2">Action:</label>
          <select
            value={action}
            onChange={(e) => setAction(e.target.value)}
            className="border rounded px-2 py-1"
          >
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>
        <button type="submit" className="bg-primary text-white px-4 py-2 rounded">
          Execute Trade
        </button>
      </form>
      {result && (
        <div>
          <h2 className="text-xl font-semibold mb-2">Result:</h2>
          <p>Status: {result.status}</p>
          <p>Message: {result.message}</p>
          {result.transaction_id && <p>Transaction ID: {result.transaction_id}</p>}
        </div>
      )}
    </div>
  );
}

export default TradingAgent;

