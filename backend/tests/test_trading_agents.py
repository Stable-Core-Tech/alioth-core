import pytest
from app.ai import trading_agents

def test_execute_trade():
    result = trading_agents.execute_trade('BTC', 1.5, 'buy')
    assert result['status'] == 'success'
    assert 'transaction_id' in result

    result = trading_agents.execute_trade('ETH', 2.0, 'invalid')
    assert result['status'] == 'error'

