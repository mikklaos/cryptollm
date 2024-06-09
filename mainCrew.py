import re
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai_tools import tool
from langchain.agents import load_tools
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_groq import ChatGroq
import streamlit as st

from selected_coin import selected_coin, completed
from tools.price_tools import cryptocurrency_price_tool
from tools.search_tools import cryptocurrency_news_tool
from tools.search_tools import ExaSearch, TavilySearch


class CryptoAgents:
    def __init__(self):
        self.exa = ExaSearch()
        self.tavily = TavilySearch()

    def customer_communicator(self, llm):
        return Agent(
            role="Senior cryptocurrency customer communicator",
            goal="Find which cryptocurrency the customer is interested in. Example: customer types in BTC or bitcoin output will be BTC. Output should be the cryptocurrency symbol.",
            backstory="""You're highly experienced in communicating about cryptocurrencies and blockchain technology with customers and their research needs""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            max_iter=5,
            memory=True,
            step_callback=set_correct_coin_name,
            human_input=True
        )

    def news_analyst(self, llm, timeframe=60):
        return Agent(
            role="Cryptocurrency News Analyst",
            goal=f"""Get news for a given cryptocurrency. Write 1 paragraph analysis of the market and make prediction - up, down or neutral. """,
            backstory="""You're an expert analyst of trends based on cryptocurrency news. You have a complete understanding of macroeconomic factors, but you specialize into analyzing news.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            max_iter=5,
            memory=True,
            step_callback=streamlit_callback,
            tools=[self.tavily],
        )

    def price_analyst(self, llm, timeframe=60):
        return Agent(
            role="Cryptocurrency Price Analyst",
            goal=f"""Get historical prices for a given cryptocurrency. Write 1 paragraph analysis of the market and give me entry and exit prices including stop loss. Include important support and resitance levels. Make sure analysis is based on {timeframe} of data""",
            backstory="""You're an expert analyst of trends based on cryptocurrency historical prices. You have a complete understanding of macroeconomic factors, but you specialize into technical analys based on historical prices.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            max_iter=5,
            memory=True,
            step_callback=streamlit_callback,
            tools=[cryptocurrency_price_tool],
        )

    def writer(self, llm, timeframe=60):
        return Agent(
            role="Cryptocurrency Report Writer",
            goal=f"""Write 3 paragraph report for {timeframe} of data. Report should help user to make investment decision for {timeframe}. First paragraph with important news and trends. Second paragraph with 5 important bulletpoints of the cryptocurrency market in markdown format. Third paragraph should have 3 bulletpoints: entry price, stopp loss, takeprofit price. Make sure that output Include a prediction for the future trend - up, down or neutral. Use emojis to make the report more engaging.The output should be presented in Markdown format without using LaTEx notation""",
            backstory="""You're widely accepted as the best cryptocurrency analyst that understands the market and have tracked every asset for more than 10 years. Your trends analysis are always extremely accurate. You're also master level analyst in the traditional markets and have deep understanding of human psychology. You understand macro factors and combine those multiple theories - e.g. cycle theory. You're able to hold multiple opininons when analysing anything. You understand news and historical prices, but you look at those with a healthy dose of skepticism. You also consider the source of news articles. Your most well developed talent is providing clear and concise summarization that explains very complex market topics in simple to understand terms. Some of your writing techniques include: - Creating a bullet list (executive summary) of the most importannt points - Distill complex analyses to their most important parts You writing transforms even dry and most technical texts into a pleasant and interesting read.""",
            llm=llm,
            verbose=True,
            max_iter=5,
            memory=True,
            step_callback=streamlit_callback,
            allow_delegation=False,
        )


def set_correct_coin_name(step_output):
    selected_coin.coin = step_output.return_values.get('output')


def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
    st.markdown("---")
    for step in step_output:
        if isinstance(step, tuple) and len(step) == 2:
            action, observation = step
            if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
                st.markdown(f"# Action")
                st.markdown(f"**Tool:** {action['tool']}")
                st.markdown(f"**Tool Input** {action['tool_input']}")
                st.markdown(f"**Log:** {action['log']}")
                st.markdown(f"**Action:** {action['Action']}")
                st.markdown(
                    f"**Action Input:** ```json\n{action['tool_input']}\n```")
            elif isinstance(action, str):
                st.markdown(f"**Action:** {action}")
            else:
                st.markdown(f"**Action:** {str(action)}")

            st.markdown(f"**Observation**")
            if isinstance(observation, str):
                observation_lines = observation.split('\n')
                for line in observation_lines:
                    if line.startswith('Title: '):
                        st.markdown(f"**Title:** {line[7:]}")
                    elif line.startswith('Link: '):
                        st.markdown(f"**Link:** {line[6:]}")
                    elif line.startswith('Snippet: '):
                        st.markdown(f"**Snippet:** {line[9:]}")
                    elif line.startswith('-'):
                        st.markdown(line)
                    else:
                        st.markdown(line)
            else:
                st.markdown(str(observation))
        else:
            st.markdown(step)
        completed.agents = completed.agents + 1
