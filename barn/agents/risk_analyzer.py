import numpy as np
from typing import Dict, List
from .base import BaseAgent

class RiskAnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing token risks."""
    
    def __init__(self, name: str, config: Dict = None):
        super().__init__(name, config)
        self.risk_metrics = {
            'volatility': self._calculate_volatility,
            'sharpe_ratio': self._calculate_sharpe_ratio,
            'value_at_risk': self._calculate_var
        }
    
    async def process(self, price_data: List[float]) -> Dict[str, float]:
        """Process token price data and return risk metrics."""
        results = {}
        for metric_name, metric_func in self.risk_metrics.items():
            results[metric_name] = metric_func(price_data)
        return results
    
    async def run(self) -> Dict[str, float]:
        """Run risk analysis on current state data."""
        if 'price_data' not in self.state:
            raise ValueError("No price data available in state")
        return await self.process(self.state['price_data'])
    
    def _calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility."""
        returns = np.diff(prices) / prices[:-1]
        return float(np.std(returns))
    
    def _calculate_sharpe_ratio(self, prices: List[float], risk_free_rate: float = 0.01) -> float:
        """Calculate Sharpe ratio."""
        returns = np.diff(prices) / prices[:-1]
        excess_returns = returns - risk_free_rate
        if len(excess_returns) == 0:
            return 0.0
        return float(np.mean(excess_returns) / np.std(excess_returns))
    
    def _calculate_var(self, prices: List[float], confidence: float = 0.95) -> float:
        """Calculate Value at Risk."""
        returns = np.diff(prices) / prices[:-1]
        return float(np.percentile(returns, (1 - confidence) * 100))

