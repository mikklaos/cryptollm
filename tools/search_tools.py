from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from crewai_tools import BaseTool
import os
import requests, json
from datetime import datetime, timedelta

from tavily import TavilyClient

search_tool = DuckDuckGoSearchResults(backend="news", num_results=10)


@tool("search tool")
def cryptocurrency_news_tool(ticker_symbol: str) -> str:
    """Get news for a given cryptocurrency ticker symbol"""
    return search_tool.run(ticker_symbol + " cryptocurrency")


class PerplexitySearch(BaseTool):
    name: str = "Perplexity Search"
    description: str = "Provides detailed AI-generated answers and insights from the Perplexity API, including citations."

    def _run(self, user_query: str) -> str:
        perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        if not perplexity_api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set")
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "sonar-medium-online",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an artificial intelligence assistant and you need to "
                        "engage in a helpful, detailed, polite conversation with a user."
                    ),
                },
                {
                    "role": "user",
                    "content": user_query,
                },
            ],
            "return_citations": True
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {perplexity_api_key}"
        }
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        content = response_json['choices'][0]['message']['content'] if response_json[
            'choices'] else "No content available"
        citations = "\n\nCitations:\n" + "\n".join(response_json.get('citations', [])) if response_json.get(
            'citations') else ""
        return f"{content}{citations}"


class YouSearch(BaseTool):
    name: str = "You Search"
    description: str = "Fetches data from the YDC Index API based on the provided query."

    def _run(self, query: str, fetch_raw: bool = False) -> str:
        you_api_key = os.getenv("YOU_API_KEY")
        if not you_api_key:
            raise ValueError("YOU_API_KEY environment variable not set")
        url = "https://api.ydc-index.io/search"
        querystring = {"query": query, "num_web_results": 10}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=querystring)
        if fetch_raw:
            return response.text
        else:
            data = response.json()
            formatted_response = json.dumps(data, indent=4)
            return formatted_response


class ExaSearch(BaseTool):
    name: str = "Exa Search"
    description: str = "Performs a search with the Exa API using a prompt-engineered query, retrieves relevant results, and summarizes each result using an LLM."

    def _run(self, query: str) -> str:
        exa_api_key = os.getenv("EXA_API_KEY")
        if not exa_api_key:
            raise ValueError("EXA_API_KEY environment variable not set")
        url = "https://api.exa.ai/search"
        start_published_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        payload = {
            "query": query,
            "useAutoprompt": False,
            "num_results": 5,
            "startPublishedDate": start_published_date,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": exa_api_key
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return json.dumps(response.json().get('results', []), indent=4)
        else:
            return f"Failed to fetch search results: {response.text}"


class TavilySearch(BaseTool):
    name: str = "Tavily Search"
    description: str = "Performs a comprehensive search using the Tavily API and returns a summary of results. Example  query 'Should I invest in Apple in 2024?'"

    def _run(self, query: str) -> str:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        tavily = TavilyClient(api_key=tavily_api_key)

        # Assuming the TavilySearchResults class exists and works as expected.
        # The implementation details for invoking the Tavily API are omitted for brevity.
        return tavily.search(query=query)


class YouSummarize(BaseTool):
    name: str = "You Summarize"
    description: str = "Summarizes the top results from a You.com search query."

    def _run(self, query: str, num_results: int = 5) -> str:
        # Placeholder for You.com API call and summarization
        # The actual implementation would involve fetching search results and summarizing them.
        return "Summarized search results"


class YouFetchRaw(BaseTool):
    name: str = "You Fetch Raw"
    description: str = "Fetches raw search results from You.com for a given query."

    def _run(self, query: str) -> str:
        # Placeholder for You.com raw search results fetching
        return "Raw search results"


class ExaFindSimilar(BaseTool):
    name: str = "Exa Find Similar"
    description: str = "Finds similar links to the provided URL using the Exa API."

    def _run(self, url: str) -> str:
        # Placeholder for Exa API call to find similar links
        return "Similar links from Exa API"
