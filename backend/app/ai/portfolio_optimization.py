import numpy as np
from typing import Dict, List

def optimize_portfolio(portfolio: Dict[str, float], risk_tolerance: float) -> Dict[str, float]:
    tokens = list(portfolio.keys())
    current_allocation = np.array(list(portfolio.values()))
    
    # This is a simplified optimization strategy
    # In a real-world scenario, you'd use more sophisticated methods
    total = sum(current_allocation)
    risk_scores = np.random.rand(len(tokens))  # In reality, these would be calculated
    
    new_allocation = risk_scores * risk_tolerance
    new_allocation = new_allocation / sum(new_allocation) * total
    
    return dict(zip(tokens, new_allocation.tolist()))

