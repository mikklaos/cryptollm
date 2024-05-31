import pandas as pd
import requests
from langchain.tools import tool
import os


def get_daily_closing_prices(ticker) -> pd.DataFrame:
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market=USD&apikey={os.environ["ALPHAVANTAGE_API_KEY"]}'
    response = requests.get(url)
    data = response.json()
    price_data = data["Time Series (Digital Currency Daily)"]
    daily_close_prices = {
        date: prices["4. close"] for (date, prices) in price_data.items()
    }

    df = pd.DataFrame.from_dict(daily_close_prices, orient="index", columns=["price"])
    df.index = pd.to_datetime(df.index)
    df["price"] = pd.to_numeric(df["price"])

    return df


@tool("price tool")
def cryptocurrency_price_tool(ticker_symbol: str) -> str:
    """Get daily closing price for a given cryptocurrency ticker symbol for the previous 60 days"""
    price_df = get_daily_closing_prices(ticker_symbol)
    text_output = []
    for date, row in price_df.head(60).iterrows():
        text_output.append(f"{date.strftime('%Y-%m-%d')} - {row['price']:.2f}")
    return "\n".join(text_output)
