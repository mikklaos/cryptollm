from crewai import Crew, Process
from mainCrew import CryptoAgents
from cryptoTasks import CryptoTasks
import streamlit as st
import streamlit.components.v1 as components
from langchain_groq import ChatGroq
import datetime

st.set_page_config(page_icon="✈️", layout="wide")


# https://github.com/tonykipkemboi/trip_planner_agent/blob/main/streamlit_app.py
# https://github.com/amadad/civic-agentcy/blob/main/src/civic_agentcy/tools/search_tools.py

widget_width = 980
def tradingview_chart(symbol):
    """Shows a TradingView chart."""
    components.html(
        f"""
         <div style="display: flex; justify-content: flex-start;">
        <div class="tradingview-widget-container" align="left" >
            <div id="tradingview_1c6e3" ></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget(
            {{
            "width": {widget_width},
            "height": 610,
            "symbol": "{symbol}",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "studies": [
                "ROC@tv-basicstudies",
            ],
            "custom_font_family": 'Roboto',
            "container_id": "tradingview_1c6e3"
            }}
            );
            </script>
        </div>
        </div>
        
        """,
        height=700,
    )


def get_info_widget(
        ticker: str = "AAPL",
        theme: str = "dark",
):
    width = widget_width
    height = 200

    header = '''
        <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
    '''

    footer = '''
        </script>
        </div>
    '''

    widget = {
        "symbol": ticker,
        "height": height,
        "width": width,
        "locale": "en",
        "colorTheme": theme,
        "isTransparent": False
    }

    widget = (
        str(widget)
        .replace('True', 'true')
        .replace('False', 'false')
        .replace('\'', '"')
    )

    return (
        header + widget + footer,
        width,
        height,
    )




tradingview_chart("BTCUSD")



def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class CryptoCrew:

    def __init__(self, coin, timeframe):
        self.output_placeholder = st.empty()
        self.coin = coin
        self.timeframe = timeframe
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

    def run(self):
        agents = CryptoAgents()
        tasks = CryptoTasks()

        customer_communicator = agents.customer_communicator(self.llm)
        price_analyst = agents.price_analyst(self.llm, self.timeframe)
        news_analyst = agents.news_analyst(self.llm)
        writer = agents.writer(self.llm)

        get_cryptocurrency_task = tasks.get_cryptocurrency(
            customer_communicator, self.coin
        )

        get_news_analysis_task = tasks.get_news_analysis(
            news_analyst, [get_cryptocurrency_task]
        )

        get_price_analysis_task = tasks.get_price_analysis(
            price_analyst, [get_cryptocurrency_task]
        )

        write_report_task = tasks.write_report(
            writer, [get_news_analysis_task, get_price_analysis_task]
        )

        crew = Crew(
            agents=[customer_communicator, price_analyst, news_analyst, writer],
            tasks=[get_cryptocurrency_task, get_news_analysis_task, get_price_analysis_task, write_report_task],
            verbose=2,
            process=Process.sequential,
            full_output=True,
            share_crew=False,
            manager_llm=self.llm,
            max_iter=15,
        )

        result = crew.kickoff()
        self.output_placeholder.markdown(result)

        return result


if __name__ == "__main__":
    icon("💵 CryptoAI")

    st.subheader("Crypto price prediction bot!",
                 divider="rainbow", anchor=False)
    submitted = None

    if not submitted:
        # Create an explanation section with emojis and markdown of agents and tasks. Describe using visual elements.
        # st.markdown("### How it works", unsafe_allow_html=True)

        st.markdown(
            """
            ##### Multi Agent AI model
            - **Customer Communicator 🤖**: Communicates with the customer to get the cryptocurrency to analyze.⬇️
            - **Price Analysis 🤖**: Analyzes the historical price of a cryptocurrency to predict its future price. ⬇️
            - **News Analysis 🤖**: Analyzes the news related to a cryptocurrency to predict its future price.⬇️
            - **Writer 🤖**: Writes a report based on the price and news analysis.✅
            """
        )

    today = datetime.datetime.now().date()
    next_year = today.year + 1
    jan_16_next_year = datetime.date(next_year, 1, 10)

    with st.sidebar:
        st.header("👇 Enter crypto to analyze")
        with st.form("my_form"):
            coin = st.text_input(
                "What crypto you want to analyse?", placeholder=" eg. Bitcoin, Ethereum, Dogecoin")

            # Define the options in months and corresponding days
            options = {
                "1 month": 30,
                "2 months": 60,
                "6 months": 180,
                "8 months": 240,
                "1 year": 365
            }

            # Create a dropdown menu with the options
            timeframe = st.selectbox("How long do you wish to invest?", list(options.keys()))

            submitted = st.form_submit_button("Submit")

        st.divider()

        # Credits to joaomdmoura/CrewAI for the code: https://github.com/joaomdmoura/crewAI

        st.sidebar.info(
            """
        Analyze the price of a cryptocurrency and predict its future price using **Multi Agent AI model** 
        """,
            icon="🚀"
        )

if submitted:
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=500, border=False):
            trip_crew = CryptoCrew(coin, timeframe)
            result = trip_crew.run()
        status.update(label=f"✅ {coin} analysis Ready!",
                      state="complete", expanded=False)

    st.subheader(f"Here is your {coin} analysis", anchor=False, divider="rainbow")

    st.markdown("### Analysis Result", unsafe_allow_html=True)
    info, info_width, info_height = get_info_widget(
        ticker="BTCUSD",
        theme="light",

    )

    components.html(
        info,
        height=info_height,
        width=info_width,
    )


    # Assuming crew_result is a string. If it's not, you might need to convert or format it accordingly.
    st.markdown(f"<div style='white-space: pre-wrap;'>{result.get('final_output')}</div>", unsafe_allow_html=True)
