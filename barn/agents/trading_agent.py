from typing import Dict, List, Optional
from .base import BaseAgent
import numpy as np

class TradingAgent(BaseAgent):
    """Agent responsible for executing trades based on risk analysis."""
    
    def __init__(self, name: str, config: Dict = None):
        super().__init__(name, config)
        self.position_size = 0
        self.trades_history: List[Dict] = []
        
    async def process(self, signal_data: Dict) -> Dict:
        """Process trading signals and execute trades."""
        action = self._determine_action(signal_data)
        if action['should_trade']:
            trade_result = await self._execute_trade(action)
            self.trades_history.append(trade_result)
            return trade_result
        return {"action": "hold", "reason": action['reason']}
    
    async def run(self) -> Dict:
        """Run trading logic based on current state."""
        if 'signal_data' not in self.state:
            raise ValueError("No signal data available in state")
        return await self.process(self.state['signal_data'])
    
    def _determine_action(self, signal_data: Dict) -> Dict:
        """Determine trading action based on signals."""
        risk_score = signal_data.get('risk_score', float('inf'))
        price_trend = signal_data.get('price_trend', 0)
        
        if risk_score > self.config.get('max_risk_threshold', 0.8):
            return {
                "should_trade": False,
                "reason": "Risk too high"
            }
            
        return {
            "should_trade": True,
            "action": "buy" if price_trend > 0 else "sell",
            "size": self._calculate_position_size(risk_score)
        }
    
    def _calculate_position_size(self, risk_score: float) -> float:
        """Calculate appropriate position size based on risk."""
        base_size = self.config.get('base_position_size', 1.0)
        risk_factor = 1 - risk_score
        return base_size * risk_factor
    
    async def _execute_trade(self, action: Dict) -> Dict:
        """Execute the trade and return results."""
        # In a real implementation, this would interact with an exchange API
        trade_result = {
            "timestamp": np.datetime64('now'),
            "action": action['action'],
            "size": action['size'],
            "status": "executed",
            "transaction_id": f"tx_{len(self.trades_history)}"
        }
        
        if action['action'] == 'buy':
            self.position_size += action['size']
        else:
            self.position_size -= action['size']
            
        return trade_result

