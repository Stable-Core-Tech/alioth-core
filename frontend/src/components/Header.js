import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-primary text-white p-4">
      <nav className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">Barn System</Link>
        <ul className="flex space-x-4">
          <li><Link to="/risk-assessment">Risk Assessment</Link></li>
          <li><Link to="/trading-agent">Trading Agent</Link></li>
          <li><Link to="/portfolio-optimization">Portfolio Optimization</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;

