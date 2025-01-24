from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass

@dataclass
class RiskMetrics:
    token: str
    volatility: float
    var: float  # Value at Risk
    expected_shortfall: float
    liquidity_score: float
    timestamp: datetime

class RiskManager:
    """Advanced risk management and monitoring system"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self._risk_metrics: Dict[str, List[RiskMetrics]] = {}
        self._risk_limits: Dict[str, float] = {}
        self._last_update: Optional[datetime] = None
        
    def update_metrics(self, metrics: RiskMetrics) -> None:
        """Update risk metrics for a token"""
        if metrics.token not in self._risk_metrics:
            self._risk_metrics[metrics.token] = []
            
        self._risk_metrics[metrics.token].append(metrics)
        self._last_update = datetime.now()
        
        # Maintain history window
        window_days = self.config.get("risk_window_days", 30)
        cutoff = datetime.now() - timedelta(days=window_days)
        
        self._risk_metrics[metrics.token] = [
            m for m in self._risk_metrics[metrics.token]
            if m.timestamp > cutoff
        ]
    
    def set_risk_limit(self, token: str, limit: float) -> None:
        """Set risk limit for a token"""
        self._risk_limits[token] = limit
    
    def check_risk_breach(self, token: str) -> Optional[Dict]:
        """Check if current risk metrics breach limits"""
        if token not in self._risk_metrics or not self._risk_metrics[token]:
            return None
            
        current_metrics = self._risk_metrics[token][-1]
        limit = self._risk_limits.get(token)
        
        if limit is None:
            return None
            
        composite_risk = self._calculate_composite_risk(current_metrics)
        
        if composite_risk > limit:
            return {
                "token": token,
                "risk_level": composite_risk,
                "limit": limit,
                "breach_amount": composite_risk - limit,
                "timestamp": datetime.now()
            }
            
        return None
    
    def get_risk_report(self) -> Dict:
        """Generate comprehensive risk report"""
        report = {
            "timestamp": datetime.now(),
            "global_metrics": self._calculate_global_metrics(),
            "token_metrics": {},
            "risk_breaches": [],
            "trend_analysis": {}
        }
        
        for token in self._risk_metrics:
            if not self._risk_metrics[token]:
                continue
                
            metrics = self._risk_metrics[token]
            report["token_metrics"][token] = self._calculate_token_metrics(metrics)
            
            breach = self.check_risk_breach(token)
            if breach:
                report["risk_breaches"].append(breach)
                
            report["trend_analysis"][token] = self._analyze_risk_trends(metrics)
            
        return report
    
    def _calculate_composite_risk(self, metrics: RiskMetrics) -> float:
        """Calculate composite risk score from multiple metrics"""
        weights = self.config.get("risk_weights", {
            "volatility": 0.3,
            "var": 0.3,
            "expected_shortfall": 0.2,
            "liquidity": 0.2
        })
        
        # Normalize metrics to 0-1 scale
        normalized = {
            "volatility": min(metrics.volatility * 10, 1),
            "var": min(abs(metrics.var) * 5, 1),
            "expected_shortfall": min(abs(metrics.expected_shortfall) * 5, 1),
            "liquidity": 1 - metrics.liquidity_score
        }
        
        return sum(
            normalized[key] * weight
            for key, weight in weights.items()
        )
    
    def _calculate_global_metrics(self) -> Dict:
        """Calculate system-wide risk metrics"""
        all_risks = []
        
        for token_metrics in self._risk_metrics.values():
            if not token_metrics:
                continue
            all_risks.append(
                self._calculate_composite_risk(token_metrics[-1])
            )
            
        if not all_risks:
            return {
                "average_risk": 0,
                "max_risk": 0,
                "risk_concentration": 0
            }
            
        return {
            "average_risk": float(np.mean(all_risks)),
            "max_risk": float(np.max(all_risks)),
            "risk_concentration": float(np.std(all_risks))
        }
    
    def _calculate_token_metrics(self, metrics: List[RiskMetrics]) -> Dict:
        """Calculate detailed metrics for a token"""
        recent = metrics[-1]
        
        return {
            "current_risk": self._calculate_composite_risk(recent),
            "volatility_trend": self._calculate_metric_trend(
                [m.volatility for m in metrics]
            ),
            "var_trend": self._calculate_metric_trend(
                [m.var for m in metrics]
            ),
            "liquidity_score": recent.liquidity_score,
            "metrics_timestamp": recent.timestamp
        }
    
    def _analyze_risk_trends(self, metrics: List[RiskMetrics]) -> Dict:
        """Analyze trends in risk metrics"""
        if len(metrics) < 2:
            return {"trend": "insufficient_data"}
            
        risk_scores = [
            self._calculate_composite_risk(m)
            for m in metrics
        ]
        
        trend = self._calculate_metric_trend(risk_scores)
        
        return {
            "trend_direction": "increasing" if trend > 0 else "decreasing",
            "trend_strength": abs(trend),
            "current_momentum": self._calculate_momentum(risk_scores)
        }
    
    def _calculate_metric_trend(self, values: List[float]) -> float:
        """Calculate trend in a metric using linear regression"""
        if len(values) < 2:
            return 0.0
            
        x = np.arange(len(values))
        y = np.array(values)
        z = np.polyfit(x, y, 1)
        return float(z[0])
    
    def _calculate_momentum(self, values: List[float]) -> float:
        """Calculate momentum indicator for risk metrics"""
        if len(values) < 2:
            return 0.0
            
        short_window = min(5, len(values))
        long_window = min(20, len(values))
        
        short_avg = np.mean(values[-short_window:])
        long_avg = np.mean(values[-long_window:])
        
        return float(short_avg - long_avg)

