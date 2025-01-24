import pytest
import numpy as np
from barn.agents.risk_analyzer import RiskAnalyzerAgent

@pytest.fixture
def risk_analyzer():
    return RiskAnalyzerAgent("test_analyzer")

@pytest.mark.asyncio
async def test_risk_analysis(risk_analyzer):
    # Test data
    price_data = [100, 102, 98, 103, 101]
    risk_analyzer.update_state({"price_data": price_data})
    
    # Run analysis
    results = await risk_analyzer.run()
    
    # Verify results
    assert "volatility" in results
    assert "sharpe_ratio" in results
    assert "value_at_risk" in results
    assert all(isinstance(v, float) for v in results.values())
    
@pytest.mark.asyncio
async def test_empty_data(risk_analyzer):
    with pytest.raises(ValueError):
        await risk_analyzer.run()

