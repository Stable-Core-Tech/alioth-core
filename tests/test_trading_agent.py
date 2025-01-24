import pytest
from barn.agents.trading_agent import TradingAgent

@pytest.fixture
def trading_agent():
    config = {
        "max_risk_threshold": 0.8,
        "base_position_size": 1.0
    }
    return TradingAgent("test_trader", config)

@pytest.mark.asyncio
async def test_trading_decision(trading_agent):
    # Test data
    signal_data = {
        "risk_score": 0.5,
        "price_trend": 1.0
    }
    trading_agent.update_state({"signal_data": signal_data})
    
    # Execute trade
    result = await trading_agent.run()
    
    # Verify result
    assert "status" in result
    assert "transaction_id" in result
    assert result["status"] == "executed"
    
@pytest.mark.asyncio
async def test_high_risk_no_trade(trading_agent):
    # Test data with high risk
    signal_data = {
        "risk_score": 0.9,
        "price_trend": 1.0
    }
    trading_agent.update_state({"signal_data": signal_data})
    
    # Execute trade
    result = await trading_agent.run()
    
    # Verify result
    assert result["action"] == "hold"
    assert "Risk too high" in result["reason"]

