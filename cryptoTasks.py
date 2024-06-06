from datetime import datetime

from crewai import Task


class CryptoTasks:

    def get_cryptocurrency(self, agent, cryptocurrency_symbol):
        return Task(
            description=f"Ask which cryptocurrency the customer is interested in. {cryptocurrency_symbol} is the symbol of the cryptocurrency.",
            expected_output="Cryptocurrency symbol that the human wants you to research e.g. BTC.Example: customer types in BTC or bitcoin output will be BTC. Customer types in algorand output will be algo",
            agent=agent,
        )

    def get_news_analysis(self, agent, context):
        return Task(
            description=f"Use the search tool to get news for the cryptocurrency. The current date is {datetime.now()}. Compose the results into a helpful report.",
            expected_output="Create 1 paragraph report for the cryptocurrency, along with a prediction for the future trend.",
            agent=agent,
            context=context,
        )

    def get_price_analysis(self, agent, context):
        return Task(
            description=f"Use the price tool to get historical prices. The current date is {datetime.now()}. Compose the results into a helpful report.",
            expected_output="Create 1 paragraph summary for the cryptocurrency, along with a prediction for the future trend.",
            agent=agent,
            context=context,
        )

    def write_report(self, agent, context):
        return Task(
            description="Use the reports from the news analyst and the price analyst to create a report that summarizes the cryptocurrency.",
            expected_output="1 paragraph report that summarizes the market and predicts the future prices (trend) for the cryptocurrency. The advisor should provide specific entry points for each strategy, along with the corresponding stop loss and take profit prices.",
            agent=agent,
            context=context,
        )
