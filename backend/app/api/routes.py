from fastapi import APIRouter, HTTPException
from app.ai import risk_assessment, trading_agents, portfolio_optimization
from typing import Dict, List

router = APIRouter()

@router.post("/risk-assessment")
async def get_risk_assessment(token_data: List[Dict[str, float]]):
    return risk_assessment.assess_risk(token_data)

@router.post("/execute-trade")
async def execute_trade(token: str, amount: float, action: str):
    return trading_agents.execute_trade(token, amount, action)

@router.post("/optimize-portfolio")
async def optimize_portfolio(portfolio: Dict[str, float], risk_tolerance: float):
    if risk_tolerance < 0 or risk_tolerance > 1:
        raise HTTPException(status_code=400, detail="Risk tolerance must be between 0 and 1")
    return portfolio_optimization.optimize_portfolio(portfolio, risk_tolerance)

