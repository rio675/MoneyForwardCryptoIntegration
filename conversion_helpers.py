"""module providing a currency conversion functions"""
import requests

from requests import Session

def convert_to_jpy(coinmarketcap_api_key, amount, symbol):
    """
    a function to convert bnbx to jpy with the current exchange rate
    """
    api_url = "https://pro-api.coinmarketcap.com/v2/tools/price-conversion"

    params = {
        "symbol": symbol,
        "amount": amount,
        "convert": "JPY"
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": coinmarketcap_api_key
    }

    session = Session()
    session.headers.update(headers)

    # Specify a timeout value in seconds (e.g., 10 seconds)
    timeout_seconds = 10

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=timeout_seconds)
        # Continue processing the response here
    except requests.Timeout:
        print("The request to the API timed out.")
    except requests.RequestException as error:
        print(f"An error occurred: {error}")

    if response.status_code == 200:
        data = response.json()
        try:
            # 'price' の整数部分を取得
            integer_price = int(data["data"][0]["quote"]["JPY"]["price"])
            return integer_price
        except (KeyError, ValueError):
            return None
    else:
        print("API Request Failed. Status Code:", response.status_code)
        print("API Response:")
        try:
            print(response.json())  # エラーレスポンスを表示
        except ValueError:
            print(response.text)  # エラーレスポンスがJSONでない場合、テキストとして表示
        return None

def smallest_decimal_to_normal(balance, decimal_places):
    """
    a function to convert the smallest decimal representation to a normal decimal representation
    """
    return balance / (10 ** decimal_places)

def truncate_to_range(number, min_value=1e-8, max_value=1000000000000):
    """
    a function to truncate value into API range
    """
    # Coin market cap API指定範囲内に収まるように数値を制限
    if number < min_value:
        number = min_value
    elif number > max_value:
        number = max_value

    # 数値を小数点以下8桁まで切り捨て
    number = round(number, 8)

    return str(number)
