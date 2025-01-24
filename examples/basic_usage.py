import asyncio
from barn import BarnOrchestrator

async def main():
    # Initialize the Barn System
    config = {
        "risk_analyzer": {
            "max_lookback_periods": 30
        },
        "trader": {
            "max_risk_threshold": 0.8,
            "base_position_size": 1.0
        },
        "portfolio_manager": {
            "risk_free_rate": 0.01,
            "rebalance_threshold": 0.01
        }
    }
    
    barn = BarnOrchestrator(config)
    barn.initialize_agents()
    
    # Sample market data
    market_data = {
        "portfolio": {
            "BTC": 1.5,
            "ETH": 10.0,
            "SOL": 50.0
        },
        "historical_returns": {
            "BTC": [0.01, -0.02, 0.03, 0.01, -0.01],
            "ETH": [0.02, -0.01, 0.02, -0.02, 0.01],
            "SOL": [0.03, -0.03, 0.04, -0.01, 0.02]
        }
    }
    
    # Run the system
    results = await barn.run(market_data)
    
    # Print results
    print("\nRisk Analysis:")
    print(results["risk_analysis"])
    
    print("\nTrade Decision:")
    print(results["trade_decision"])
    
    print("\nPortfolio Update:")
    print(results["portfolio_update"])

if __name__ == "__main__":
    asyncio.run(main())

