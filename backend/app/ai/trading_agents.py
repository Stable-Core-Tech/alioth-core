from typing import Dict

def execute_trade(token: str, amount: float, action: str) -> Dict[str, str]:
    # In a real implementation, this would interact with an exchange API
    if action not in ['buy', 'sell']:
        return {'status': 'error', 'message': 'Invalid action. Use "buy" or "sell".'}
    
    return {
        'status': 'success',
        'message': f'Successfully {action}ed {amount} of {token}',
        'transaction_id': '0x1234567890abcdef'  # This would be a real transaction ID in production
    }

