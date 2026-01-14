# Implement Polymarket Agent

## 1. Backend Implementation
### 1.1 Create Polymarket Agent Package
- Create directory `python/valuecell/agents/polymarket_agent`
- Implement `python/valuecell/agents/polymarket_agent/__init__.py`
- Implement `python/valuecell/agents/polymarket_agent/tools.py`:
  - `search_markets(query: str)`: Search Polymarket markets
  - `get_market_details(market_id: str)`: Get market details
  - `get_trending_markets()`: Get trending markets
- Implement `python/valuecell/agents/polymarket_agent/prompts.py`:
  - Define system instructions for the agent
- Implement `python/valuecell/agents/polymarket_agent/core.py`:
  - `PolymarketAgent` class inheriting from `BaseAgent`
  - Initialize with Polymarket tools

### 1.2 Configure Agent
- Create `python/configs/agents/polymarket_agent.yaml`:
  - Define model configuration
  - Define capabilities and tools
- Create `python/configs/agent_cards/polymarket_agent.json`:
  - Define agent metadata (name, description, capabilities)

## 2. UI Integration
### 2.1 Add Agent Icon
- Copy an existing agent icon to `frontend/src/assets/png/agents/PolymarketAgent.png` (using `RunCommand` to copy `NewsAgent.png` as placeholder)

### 2.2 Verify Agent Registration
- Since I cannot interactively restart the server or run the init script easily, I will rely on the auto-discovery if available, or I will try to run the `init_db` script via `uv run`.

## 3. Verification
- Verify the files are created correctly.
- If possible, run a test script to verify the agent can be initialized and tools work.
