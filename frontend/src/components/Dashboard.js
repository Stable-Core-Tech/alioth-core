import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard() {
  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-4">Welcome to Barn System</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/risk-assessment" className="bg-secondary p-4 rounded shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Risk Assessment</h2>
          <p>Analyze and assess the risk of your tokens.</p>
        </Link>
        <Link to="/trading-agent" className="bg-secondary p-4 rounded shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Trading Agent</h2>
          <p>Execute trades using our AI-powered trading agent.</p>
        </Link>
        <Link to="/portfolio-optimization" className="bg-secondary p-4 rounded shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Portfolio Optimization</h2>
          <p>Optimize your portfolio based on your risk tolerance.</p>
        </Link>
      </div>
    </div>
  );
}

export default Dashboard;

