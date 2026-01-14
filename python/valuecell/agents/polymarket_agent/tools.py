"""Polymarket tools for the Polymarket Agent."""

import httpx
from loguru import logger
from typing import List, Dict, Any, Optional

BASE_URL = "https://gamma-api.polymarket.com"

async def search_markets(query: str, limit: int = 10) -> str:
    """Search for active markets on Polymarket.

    Args:
        query: The search query string.
        limit: Maximum number of results to return (default: 10).

    Returns:
        A formatted string containing the list of markets found.
    """
    url = f"{BASE_URL}/markets"
    params = {
        "limit": limit,
        "active": "true",
        "closed": "false",
        "q": query
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return "No markets found matching the query."
            
            markets = []
            for item in data:
                market_info = (
                    f"ID: {item.get('id')}\n"
                    f"Question: {item.get('question')}\n"
                    f"Outcomes: {item.get('outcomes')}\n"
                    f"Outcome Prices: {item.get('outcomePrices')}\n"
                    f"Volume: ${item.get('volume')}\n"
                    f"End Date: {item.get('endDate')}\n"
                )
                markets.append(market_info)
            
            return "\n---\n".join(markets)
            
    except Exception as e:
        logger.error(f"Error searching Polymarket: {e}")
        return f"Error searching markets: {str(e)}"

async def get_market_details(market_id: str) -> str:
    """Get detailed information about a specific market on Polymarket.

    Args:
        market_id: The unique identifier of the market.

    Returns:
        A formatted string containing detailed market information.
    """
    url = f"{BASE_URL}/markets/{market_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            item = response.json()
            
            details = (
                f"ID: {item.get('id')}\n"
                f"Question: {item.get('question')}\n"
                f"Description: {item.get('description')}\n"
                f"Category: {item.get('category')}\n"
                f"Outcomes: {item.get('outcomes')}\n"
                f"Outcome Prices: {item.get('outcomePrices')}\n"
                f"Volume: ${item.get('volume')}\n"
                f"Liquidity: ${item.get('liquidity')}\n"
                f"Start Date: {item.get('startDate')}\n"
                f"End Date: {item.get('endDate')}\n"
                f"Active: {item.get('active')}\n"
                f"Closed: {item.get('closed')}\n"
            )
            
            return details
            
    except Exception as e:
        logger.error(f"Error getting Polymarket details: {e}")
        return f"Error getting market details: {str(e)}"

async def get_trending_markets(limit: int = 10) -> str:
    """Get trending markets on Polymarket based on volume.

    Args:
        limit: Maximum number of results to return (default: 10).

    Returns:
        A formatted string containing the list of trending markets.
    """
    url = f"{BASE_URL}/markets"
    params = {
        "limit": limit,
        "active": "true",
        "closed": "false",
        "order": "volume",
        "ascending": "false"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return "No trending markets found."
            
            markets = []
            for item in data:
                market_info = (
                    f"ID: {item.get('id')}\n"
                    f"Question: {item.get('question')}\n"
                    f"Outcomes: {item.get('outcomes')}\n"
                    f"Outcome Prices: {item.get('outcomePrices')}\n"
                    f"Volume: ${item.get('volume')}\n"
                )
                markets.append(market_info)
            
            return "\n---\n".join(markets)
            
    except Exception as e:
        logger.error(f"Error fetching trending markets: {e}")
        return f"Error fetching trending markets: {str(e)}"
