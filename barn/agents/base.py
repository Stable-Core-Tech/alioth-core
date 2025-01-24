from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAgent(ABC):
    """Base agent class for all Barn System agents."""
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.state: Dict[str, Any] = {}
        
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input data and return results."""
        pass
    
    @abstractmethod
    async def run(self) -> Any:
        """Main execution loop for the agent."""
        pass
    
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update agent's internal state."""
        self.state.update(new_state)

class AgentPool:
    """Manages a pool of agents for concurrent execution."""
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
        
    def add_agent(self, agent: BaseAgent) -> None:
        """Add an agent to the pool."""
        self.agents.append(agent)
        
    def remove_agent(self, agent_name: str) -> None:
        """Remove an agent from the pool."""
        self.agents = [a for a in self.agents if a.name != agent_name]
        
    async def run_all(self) -> List[Any]:
        """Run all agents concurrently."""
        results = []
        for agent in self.agents:
            result = await agent.run()
            results.append(result)
        return results

