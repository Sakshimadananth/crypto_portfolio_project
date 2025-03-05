# # import requests

# # def fetch_crypto_data():
# #     url = "https://api.coingecko.com/api/v3/coins/markets"
# #     params = {
# #         "vs_currency": "INR",
# #         "order": "market_cap_desc",
# #         "per_page": 500,
# #         "page": 1,
# #         "sparkline": True  # Enable sparkline data
# #     }
# #     response = requests.get(url, params=params)
# #     if response.status_code == 200:
# #         return response.json()
# #     return None

# # def fetch_historical_data(symbol, days=7):
# #     url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart'
# #     params = {
# #         'vs_currency': 'inr',
# #         'days': days
# #     }
# #     response = requests.get(url, params=params)
# #     if response.status_code == 200:
# #         data = response.json()
# #         prices = [price[1] for price in data['prices']]
# #         return prices
# #     return []
# import requests

# # Function to fetch cryptocurrency data
# def fetch_crypto_data(currency="inr", per_page=500):
#     """
#     Fetches cryptocurrency market data from CoinGecko.

#     Parameters:
#         currency (str): The currency to use (e.g., 'inr', 'usd', 'eur').
#         per_page (int): Number of coins to fetch (default: 500).

#     Returns:
#         list: A list of cryptocurrency data if successful, else None.
#     """
#     url = "https://api.coingecko.com/api/v3/coins/markets"
#     params = {
#         "vs_currency": currency.lower(),
#         "order": "market_cap_desc",
#         "per_page": per_page,
#         "page": 1,
#         "sparkline": True  # Enable sparkline data for historical visualization
#     }
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching crypto data: {e}")
#         return None


# # Function to fetch historical price data
# def fetch_historical_data(symbol, days=7, currency="inr"):
#     """
#     Fetches historical price data for a specific cryptocurrency.

#     Parameters:
#         symbol (str): The CoinGecko ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
#         days (int): Number of past days for which data is required.
#         currency (str): The currency to use (e.g., 'inr', 'usd', 'eur').

#     Returns:
#         list: A list of historical prices if successful, else an empty list.
#     """
#     url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart'
#     params = {
#         'vs_currency': currency.lower(),
#         'days': days
#     }
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
#         data = response.json()
#         prices = [price[1] for price in data.get('prices', [])]
#         return prices
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching historical data for {symbol}: {e}")
#         return []
import requests

import requests
from web3 import Web3
from django.conf import settings

# Connect to Ethereum via Infura
web3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))

def get_eth_balance(wallet_address):
    """Fetch Ethereum wallet balance."""
    balance = web3.eth.get_balance(wallet_address)  # Balance in Wei
    return web3.from_wei(balance, 'ether')  # Convert to ETH

def send_eth_transaction(from_address, private_key, to_address, amount):
    """Send Ethereum transaction."""
    nonce = web3.eth.get_transaction_count(from_address)

    txn = {
        'nonce': nonce,
        'to': to_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.eth.gas_price,
        'chainId': 1  # Ethereum Mainnet
    }

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return web3.to_hex(tx_hash)


def fetch_crypto_data(currency="inr", per_page=500):
    """
    Fetches cryptocurrency market data from CoinGecko API.

    Parameters:
        currency (str): Currency code (e.g., 'inr', 'usd', 'eur').
        per_page (int): Number of records to fetch.

    Returns:
        list: Cryptocurrency data list. Returns an empty list on failure.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency.lower(),
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": True
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises exception for bad status codes
        return response.json()  # Return the data if successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cryptocurrency data: {e}")
        return []  # Always return an empty list on failure



def fetch_historical_data(symbol, days=7, currency="inr"):
    """
    Fetches historical price data for a specific cryptocurrency.

    Parameters:
        symbol (str): The CoinGecko ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
        days (int): Number of past days for which data is required.
        currency (str): The currency to use (e.g., 'inr', 'usd', 'eur').

    Returns:
        list: A list of historical prices if successful, else an empty list.
    """
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart'
    params = {
        'vs_currency': currency.lower(),
        'days': days
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract price values from the response
        prices = [price[1] for price in data.get('prices', [])]
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return []


def get_currency_symbol(currency):
    """
    Returns the currency symbol for a given currency.

    Parameters:
        currency (str): The currency code (e.g., 'inr', 'usd', 'eur').

    Returns:
        str: The currency symbol (e.g., ₹, $, €).
    """
    currency_symbols = {
        "inr": "₹",
        "usd": "$",
        "eur": "€"
    }
    return currency_symbols.get(currency.lower(), "₹")  # Default to '₹'


def fetch_coin_details(symbol):
    """
    Fetches detailed information about a specific cryptocurrency.

    Parameters:
        symbol (str): The CoinGecko ID of the cryptocurrency.

    Returns:
        dict: Detailed data of the cryptocurrency, or None on failure.
    """
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for {symbol}: {e}")
        return None
