import streamlit as st
import requests


# Function to fetch the list of cryptocurrencies from the API
@st.cache_data
def get_crypto_coins():
    url = "https://min-api.cryptocompare.com/data/all/coinlist"
    response = requests.get(url)
    data = response.json()
    return data["Data"]


def crypto_autocomplete_field():
    import streamlit as st
    import requests
    from st_aggrid import AgGrid, GridOptionsBuilder

    # Function to fetch the list of cryptocurrencies from the API
    @st.cache
    def get_crypto_coins():
        url = "https://min-api.cryptocompare.com/data/all/coinlist"
        response = requests.get(url)
        data = response.json()
        return [{"symbol": coin, "name": info["FullName"]} for coin, info in data["Data"].items()]

    # Fetching cryptocurrency coins
    crypto_coins = get_crypto_coins()

    # Streamlit app
    st.title("Cryptocurrency Autocomplete")

    # Create a DataFrame from the coins
    import pandas as pd
    df = pd.DataFrame(crypto_coins)

    # Display the DataFrame using AgGrid with a search bar
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_default_column(editable=False, filter=True)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gridOptions = gb.build()

    st.write("Search and select a cryptocurrency:")
    grid_response = AgGrid(df, gridOptions=gridOptions, height=300, width='100%', theme='streamlit')

    # Get the selected coin
    selected = grid_response['selected_rows']
    if selected:
        selected_coin = selected[0]['symbol']
        st.write(f"You selected: {selected_coin}")

    return selected
