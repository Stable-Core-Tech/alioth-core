from typing import Dict, List, Any, Optional
import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MarketSignal:
    timestamp: datetime
    token: str
    price: float
    volume: float
    indicators: Dict[str, float]

class TokenAnalysisEngine:
    """Core engine for token analysis and decision making"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = logging.getLogger("barn.engine")
        self._market_state: Dict[str, Any] = {}
        self._risk_metrics: Dict[str, float] = {}
        self._last_update: Optional[datetime] = None
        
    async def process_market_signal(self, signal: MarketSignal) -> Dict[str, Any]:
        """Process incoming market signals and generate analysis"""
        self._update_market_state(signal)
        
        analysis_tasks = [
            self._analyze_market_risk(),
            self._analyze_token_metrics(),
            self._generate_trading_signals()
        ]
        
        results = await asyncio.gather(*analysis_tasks)
        
        return {
            "risk_analysis": results[0],
            "token_metrics": results[1],
            "trading_signals": results[2],
            "timestamp": datetime.now()
        }
    
    def _update_market_state(self, signal: MarketSignal) -> None:
        """Update internal market state with new signal data"""
        if signal.token not in self._market_state:
            self._market_state[signal.token] = []
        
        self._market_state[signal.token].append({
            "timestamp": signal.timestamp,
            "price": signal.price,
            "volume": signal.volume,
            "indicators": signal.indicators
        })
        
        # Keep only recent data based on config
        window_size = self.config.get("market_window_size", 100)
        self._market_state[signal.token] = self._market_state[signal.token][-window_size:]
        self._last_update = datetime.now()

    async def _analyze_market_risk(self) -> Dict[str, float]:
        """Analyze market risk factors"""
        risk_factors = {}
        
        for token, history in self._market_state.items():
            if not history:
                continue
                
            prices = [h["price"] for h in history]
            volumes = [h["volume"] for h in history]
            
            risk_factors[token] = {
                "price_volatility": self._calculate_volatility(prices),
                "volume_trend": self._calculate_trend(volumes),
                "risk_score": self._calculate_risk_score(prices, volumes)
            }
            
        return risk_factors
    
    async def _analyze_token_metrics(self) -> Dict[str, Dict[str, float]]:
        """Analyze individual token metrics"""
        token_metrics = {}
        
        for token, history in self._market_state.items():
            if not history:
                continue
                
            recent_data = history[-1]
            token_metrics[token] = {
                "current_price": recent_data["price"],
                "current_volume": recent_data["volume"],
                "market_impact": self._calculate_market_impact(
                    recent_data["volume"],
                    recent_data["price"]
                ),
                **recent_data["indicators"]
            }
            
        return token_metrics
    
    async def _generate_trading_signals(self) -> List[Dict[str, Any]]:
        """Generate trading signals based on analysis"""
        signals = []
        risk_threshold = self.config.get("risk_threshold", 0.7)
        
        for token, history in self._market_state.items():
            if not history:
                continue
                
            risk_score = self._calculate_risk_score(
                [h["price"] for h in history],
                [h["volume"] for h in history]
            )
            
            if risk_score < risk_threshold:
                signal = {
                    "token": token,
                    "action": "ANALYZE",
                    "confidence": 1 - risk_score,
                    "timestamp": datetime.now()
                }
                signals.append(signal)
                
        return signals
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate volatility using advanced statistical methods"""
        if len(values) < 2:
            return 0.0
            
        import numpy as np
        returns = np.diff(values) / values[:-1]
        return float(np.std(returns))
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend strength using regression"""
        if len(values) < 2:
            return 0.0
            
        import numpy as np
        x = np.arange(len(values))
        y = np.array(values)
        z = np.polyfit(x, y, 1)
        return float(z[0])
    
    def _calculate_market_impact(self, volume: float, price: float) -> float:
        """Calculate market impact score"""
        base_liquidity = self.config.get("base_liquidity", 1000000)
        return (volume * price) / base_liquidity
    
    def _calculate_risk_score(self, prices: List[float], volumes: List[float]) -> float:
        """Calculate comprehensive risk score"""
        volatility = self._calculate_volatility(prices)
        volume_trend = self._calculate_trend(volumes)
        
        # Normalize components
        norm_volatility = min(volatility * 10, 1)
        norm_volume = max(min(volume_trend, 1), -1)
        
        # Weighted combination
        weights = self.config.get("risk_weights", {
            "volatility": 0.7,
            "volume_trend": 0.3
        })
        
        risk_score = (
            weights["volatility"] * norm_volatility +
            weights["volume_trend"] * (1 - abs(norm_volume))
        )
        
        return min(max(risk_score, 0), 1)

