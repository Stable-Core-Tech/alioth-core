import numpy as np
from typing import List, Dict

def assess_risk(token_data: List[Dict[str, float]]) -> Dict[str, float]:
    prices = [data['price'] for data in token_data]
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns)
    sharpe_ratio = np.mean(returns) / volatility if volatility != 0 else 0
    
    return {
        'volatility': float(volatility),
        'sharpe_ratio': float(sharpe_ratio),
        'risk_score': float(1 / (1 + sharpe_ratio))
    }

