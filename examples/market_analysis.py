import asyncio
from datetime import datetime
from barn.core import (
    TokenAnalysisEngine,
    MarketSignal,
    PortfolioOptimizer,
    Position,
    RiskManager,
    RiskMetrics
)

async def main():
    # Initialize components
    engine = TokenAnalysisEngine({
        "market_window_size": 100,
        "risk_threshold": 0.7
    })
    
    portfolio = PortfolioOptimizer({
        "max_history_length": 1000,
        "min_position_size": 0.05,
        "rebalance_threshold": 0.01
    })
    
    risk_manager = RiskManager({
        "risk_window_days": 30,
        "risk_weights": {
            "volatility": 0.3,
            "var": 0.3,
            "expected_shortfall": 0.2,
            "liquidity": 0.2
        }
    })
    
    # Sample market data
    signal = MarketSignal(
        timestamp=datetime.now(),
        token="ETH",
        price=2000.0,
        volume=1000000.0,
        indicators={
            "rsi": 65.0,
            "macd": 15.5,
            "bollinger_upper": 2050.0,
            "bollinger_lower": 1950.0
        }
    )
    
    # Process market signal
    analysis = await engine.process_market_signal(signal)
    print("\nMarket Analysis:")
    print(analysis)
    
    # Update portfolio
    position = Position(
        token="ETH",
        amount=10.0,
        entry_price=1900.0,
        current_price=2000.0,
        timestamp=datetime.now()
    )
    portfolio.update_position(position)
    
    # Optimize portfolio
    optimal_weights = portfolio.optimize_portfolio()
    print("\nOptimal Portfolio Weights:")
    print(optimal_weights)
    
    # Calculate rebalancing trades
    trades = portfolio.get_rebalancing_trades(optimal_weights)
    print("\nRebalancing Trades:")
    print(trades)
    
    # Update risk metrics
    risk_metrics = RiskMetrics(
        token="ETH",
        volatility=0.15,
        var=-0.05,
        expected_shortfall=-0.07,
        liquidity_score=0.85,
        timestamp=datetime.now()
    )
    risk_manager.update_metrics(risk_metrics)
    
    # Generate risk report
    risk_report = risk_manager.get_risk_report()
    print("\nRisk Report:")
    print(risk_report)

if __name__ == "__main__":
    asyncio.run(main())

