"""Polymarket Agent Core Implementation."""

from typing import Any, AsyncGenerator, Dict, Optional

from agno.agent import Agent
from loguru import logger

from valuecell.adapters.models import create_model_for_agent
from valuecell.config.manager import get_config_manager
from valuecell.core.agent.responses import streaming
from valuecell.core.types import BaseAgent, StreamResponse

from .prompts import POLYMARKET_AGENT_INSTRUCTIONS
from .tools import get_market_details, get_trending_markets, search_markets


class PolymarketAgent(BaseAgent):
    """Polymarket Agent for fetching and analyzing prediction markets."""

    def __init__(self, **kwargs):
        """Initialize the Polymarket Agent."""
        super().__init__(**kwargs)
        # Load agent configuration
        self.config_manager = get_config_manager()
        self.agent_config = self.config_manager.get_agent_config("polymarket_agent")

        # Load tools
        available_tools = [search_markets, get_market_details, get_trending_markets]

        # Use create_model_for_agent to load agent-specific configuration
        self.knowledge_agent = Agent(
            model=create_model_for_agent("polymarket_agent"),
            tools=available_tools,
            instructions=POLYMARKET_AGENT_INSTRUCTIONS,
            add_datetime_to_context=True,
        )

        logger.info("PolymarketAgent initialized with tools")

    async def stream(
        self,
        query: str,
        conversation_id: str,
        task_id: str,
        dependencies: Optional[Dict] = None,
    ) -> AsyncGenerator[StreamResponse, None]:
        """Stream responses."""
        logger.info(
            f"Processing polymarket query: {query[:100]}{'...' if len(query) > 100 else ''}"
        )

        try:
            response_stream = self.knowledge_agent.arun(
                query,
                stream=True,
                stream_intermediate_steps=True,
                session_id=conversation_id,
            )
            async for event in response_stream:
                if event.event == "RunContent":
                    yield streaming.message_chunk(event.content)
                elif event.event == "ToolCallStarted":
                    yield streaming.tool_call_started(
                        event.tool.tool_call_id, event.tool.tool_name
                    )
                elif event.event == "ToolCallCompleted":
                    yield streaming.tool_call_completed(
                        event.tool.result, event.tool.tool_call_id, event.tool.tool_name
                    )

            yield streaming.done()
            logger.info("Polymarket query processed successfully")

        except Exception as e:
            logger.error(f"Error processing polymarket query: {str(e)}")
            logger.exception("Full error details:")
            yield {"type": "error", "content": f"Error processing query: {str(e)}"}

    async def run(self, query: str, **kwargs) -> str:
        """Run agent and return response."""
        logger.info(
            f"Running polymarket agent with query: {query[:100]}{'...' if len(query) > 100 else ''}"
        )

        try:
            logger.debug("Starting polymarket agent processing")

            # Get the complete response from the knowledge agent
            response = await self.knowledge_agent.arun(query)

            logger.info("Polymarket agent query completed successfully")
            
            return response.content

        except Exception as e:
            logger.error(f"Error in PolymarketAgent run: {e}")
            logger.exception("Full error details:")
            return f"Error processing query: {str(e)}"

    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities."""
        return {
            "name": "Polymarket Agent",
            "description": "Agent for searching and analyzing Polymarket prediction markets",
            "tools": [
                {
                    "name": "search_markets",
                    "description": "Search for markets by keyword",
                },
                {
                    "name": "get_market_details",
                    "description": "Get detailed info about a specific market",
                },
                {
                    "name": "get_trending_markets",
                    "description": "Get trending markets by volume",
                },
            ],
            "supported_queries": [
                "Search for election markets",
                "What are the trending markets?",
                "Get details for market ID...",
            ],
        }
