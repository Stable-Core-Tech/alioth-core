from typing import Dict, List
from .base import BaseAgent
import numpy as np
from scipy.optimize import minimize

class PortfolioManagerAgent(BaseAgent):
    """Agent responsible for portfolio optimization and management."""
    
    def __init__(self, name: str, config: Dict = None):
        super().__init__(name, config)
        self.portfolio: Dict[str, float] = {}
        self.historical_returns: Dict[str, List[float]] = {}
        
    async def process(self, portfolio_data: Dict) -> Dict:
        """Process portfolio data and optimize allocations."""
        self._update_portfolio_data(portfolio_data)
        optimal_weights = self._optimize_portfolio()
        rebalancing_trades = self._calculate_rebalancing_trades(optimal_weights)
        return {
            "optimal_weights": optimal_weights,
            "rebalancing_trades": rebalancing_trades
        }
    
    async def run(self) -> Dict:
        """Run portfolio optimization based on current state."""
        if 'portfolio_data' not in self.state:
            raise ValueError("No portfolio data available in state")
        return await self.process(self.state['portfolio_data'])
    
    def _update_portfolio_data(self, portfolio_data: Dict) -> None:
        """Update portfolio and historical returns data."""
        self.portfolio = portfolio_data.get('current_allocation', {})
        self.historical_returns = portfolio_data.get('historical_returns', {})
    
    def _optimize_portfolio(self) -> Dict[str, float]:
        """Optimize portfolio weights using mean-variance optimization."""
        tokens = list(self.portfolio.keys())
        if not tokens:
            return {}
            
        # Calculate expected returns and covariance matrix
        returns_data = np.array([self.historical_returns[token] for token in tokens])
        exp_returns = np.mean(returns_data, axis=1)
        cov_matrix = np.cov(returns_data)
        
        # Define optimization constraints
        n_assets = len(tokens)
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
        ]
        bounds = tuple((0, 1) for _ in range(n_assets))  # weights between 0 and 1
        
        # Define objective function (negative Sharpe ratio)
        risk_free_rate = self.config.get('risk_free_rate', 0.01)
        def objective(weights):
            portfolio_return = np.sum(exp_returns * weights)
            portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std
            return -sharpe_ratio
        
        # Run optimization
        initial_weights = np.array([1/n_assets] * n_assets)
        result = minimize(objective, initial_weights, method='SLSQP',
                        constraints=constraints, bounds=bounds)
        
        return dict(zip(tokens, result.x))
    
    def _calculate_rebalancing_trades(self, optimal_weights: Dict[str, float]) -> List[Dict]:
        """Calculate trades needed to rebalance to optimal weights."""
        trades = []
        total_value = sum(self.portfolio.values())
        
        for token, current_amount in self.portfolio.items():
            current_weight = current_amount / total_value
            optimal_weight = optimal_weights.get(token, 0)
            
            if abs(current_weight - optimal_weight) > self.config.get('rebalance_threshold', 0.01):
                target_amount = total_value * optimal_weight
                trade_amount = target_amount - current_amount
                trades.append({
                    "token": token,
                    "action": "buy" if trade_amount > 0 else "sell",
                    "amount": abs(trade_amount)
                })
                
        return trades

