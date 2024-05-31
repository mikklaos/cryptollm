from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

search_tool = DuckDuckGoSearchResults(backend="news", num_results=10)


@tool("search tool")
def cryptocurrency_news_tool(ticker_symbol: str) -> str:
    """Get news for a given cryptocurrency ticker symbol"""
    return search_tool.run(ticker_symbol + " cryptocurrency")
