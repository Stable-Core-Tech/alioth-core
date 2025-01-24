import pytest
from app.ai import risk_assessment

def test_assess_risk():
    token_data = [
        {'price': 100},
        {'price': 102},
        {'price': 98},
        {'price': 103},
        {'price': 101}
    ]
    result = risk_assessment.assess_risk(token_data)
    
    assert 'volatility' in result
    assert 'sharpe_ratio' in result
    assert 'risk_score' in result
    assert 0 <= result['risk_score'] <= 1

