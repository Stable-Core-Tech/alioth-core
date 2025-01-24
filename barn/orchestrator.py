from typing import Dict, List, Type
from .agents.base import BaseAgent, AgentPool
from .agents.risk_analyzer import RiskAnalyzerAgent
from .agents.trading_agent import TradingAgent
from .agents.portfolio_manager import PortfolioManagerAgent
import asyncio
import logging

class BarnOrchestrator:
    """Orchestrates the interaction between different agents in the Barn System."""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.agent_pool = AgentPool()
        self.logger = logging.getLogger(__name__)
        
    def initialize_agents(self) -> None:
        """Initialize and register all required agents."""
        agent_configs = {
            RiskAnalyzerAgent: {"name": "risk_analyzer", "config": self.config.get("risk_analyzer", {})},
            TradingAgent: {"name": "trader", "config": self.config.get("trader", {})},
            PortfolioManagerAgent: {"name": "portfolio_manager", "config": self.config.get("portfolio_manager", {})}
        }
        
        for agent_class, params in agent_configs.items():
            agent = agent_class(**params)
            self.agent_pool.add_agent(agent)
            self.logger.info(f"Initialized agent: {params['name']}")
    
    async def process_market_data(self, market_data: Dict) -> Dict:
        """Process new market data through all agents."""
        results = {}
        
        # Update all agents with new market data
        for agent in self.agent_pool.agents:
            agent.update_state({"market_data": market_data})
        
        # Run risk analysis
        risk_analyzer = next(a for a in self.agent_pool.agents if isinstance(a, RiskAnalyzerAgent))
        risk_analysis = await risk_analyzer.run()
        results["risk_analysis"] = risk_analysis
        
        # Update trading agent with risk analysis
        trader = next(a for a in self.agent_pool.agents if isinstance(a, TradingAgent))
        trader.update_state({"signal_data": {"risk_score": risk_analysis.get("risk_score", 1.0)}})
        trade_decision = await trader.run()
        results["trade_decision"] = trade_decision
        
        # Update portfolio manager
        portfolio_manager = next(a for a in self.agent_pool.agents if isinstance(a, PortfolioManagerAgent))
        portfolio_manager.update_state({
            "portfolio_data": {
                "current_allocation": market_data.get("portfolio", {}),
                "historical_returns": market_data.get("historical_returns", {})
            }
        })
        portfolio_update = await portfolio_manager.run()
        results["portfolio_update"] = portfolio_update
        
        return results
    
    async def run(self, market_data: Dict) -> Dict:
        """Main execution loop for the Barn System."""
        try:
            self.logger.info("Processing market data...")
            results = await self.process_market_data(market_data)
            self.logger.info("Market data processing completed")
            return results
        except Exception as e:
            self.logger.error(f"Error in Barn System execution: {str(e)}")
            raise

