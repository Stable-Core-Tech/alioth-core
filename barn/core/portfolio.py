from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from scipy.optimize import minimize

@dataclass
class Position:
    token: str
    amount: float
    entry_price: float
    current_price: float
    timestamp: datetime

class PortfolioOptimizer:
    """Advanced portfolio optimization and management"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self._positions: Dict[str, Position] = {}
        self._historical_data: Dict[str, List[float]] = {}
        
    def update_position(self, position: Position) -> None:
        """Update or add a new position"""
        self._positions[position.token] = position
        
        if position.token not in self._historical_data:
            self._historical_data[position.token] = []
        
        self._historical_data[position.token].append(position.current_price)
        
        # Keep historical data window manageable
        max_history = self.config.get("max_history_length", 1000)
        if len(self._historical_data[position.token]) > max_history:
            self._historical_data[position.token] = self._historical_data[position.token][-max_history:]
    
    def optimize_portfolio(self) -> Dict[str, float]:
        """Optimize portfolio weights using advanced techniques"""
        if not self._positions:
            return {}
            
        returns_data = self._calculate_returns_data()
        constraints = self._generate_constraints()
        initial_weights = self._get_initial_weights()
        
        result = self._run_optimization(returns_data, constraints, initial_weights)
        
        return dict(zip(self._positions.keys(), result.x))
    
    def _calculate_returns_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate returns and covariance data"""
        returns_list = []
        
        for token in self._positions.keys():
            prices = self._historical_data[token]
            if len(prices) < 2:
                returns_list.append([0.0])
                continue
                
            returns = np.diff(prices) / prices[:-1]
            returns_list.append(returns)
        
        returns_data = np.array(returns_list)
        return returns_data
    
    def _generate_constraints(self) -> List[Dict]:
        """Generate optimization constraints"""
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
        ]
        
        # Add minimum position constraints
        min_position = self.config.get("min_position_size", 0.05)
        for i in range(len(self._positions)):
            constraints.append(
                {'type': 'ineq', 'fun': lambda x, i=i: x[i] - min_position}
            )
            
        return constraints
    
    def _get_initial_weights(self) -> np.ndarray:
        """Get initial weights for optimization"""
        n_assets = len(self._positions)
        return np.array([1/n_assets] * n_assets)
    
    def _run_optimization(
        self,
        returns_data: np.ndarray,
        constraints: List[Dict],
        initial_weights: np.ndarray
    ) -> Any:
        """Run portfolio optimization"""
        def objective(weights):
            portfolio_return = np.sum(np.mean(returns_data, axis=1) * weights)
            portfolio_vol = np.sqrt(
                np.dot(weights.T, np.dot(np.cov(returns_data), weights))
            )
            return -portfolio_return/portfolio_vol  # Negative Sharpe ratio
            
        bounds = tuple((0, 1) for _ in range(len(self._positions)))
        
        return minimize(
            objective,
            initial_weights,
            method='SLSQP',
            constraints=constraints,
            bounds=bounds
        )
    
    def get_rebalancing_trades(self, optimal_weights: Dict[str, float]) -> List[Dict]:
        """Calculate required trades for rebalancing"""
        trades = []
        total_value = sum(
            pos.amount * pos.current_price 
            for pos in self._positions.values()
        )
        
        for token, target_weight in optimal_weights.items():
            current_position = self._positions[token]
            current_value = current_position.amount * current_position.current_price
            current_weight = current_value / total_value
            
            if abs(current_weight - target_weight) > self.config.get("rebalance_threshold", 0.01):
                target_value = total_value * target_weight
                trade_amount = (target_value - current_value) / current_position.current_price
                
                trades.append({
                    "token": token,
                    "action": "buy" if trade_amount > 0 else "sell",
                    "amount": abs(trade_amount),
                    "current_price": current_position.current_price,
                    "timestamp": datetime.now()
                })
                
        return trades

