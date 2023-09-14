"""module providing a bnbx wallet balance getter"""
import requests
from requests import Session

def get_token_balance(bsc_api_key, contract_address, wallet_address):
    """
    a function to get bnbx wallet balance from address
    """
    api_url = "https://api.bscscan.com/api"

    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": wallet_address,
        "tag": "latest",
        "api_key": bsc_api_key
    }

    # Specify a timeout value in seconds (e.g., 10 seconds)
    timeout_seconds = 10

    try:
        response = requests.get(api_url, params=params, timeout=timeout_seconds)
        # Continue processing the response here
    except requests.Timeout:
        print("The request to the API timed out.")
    except requests.RequestException as error:
        print(f"An error occurred: {error}")

    if response.status_code == 200:
        data = response.json()
        if "result" in data:
            balance = data["result"]
            return balance
        else:
            return None
    else:
        return None

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

def get_bnbx_balance():
    """
    a function to get bnbx wallet balance in JPY
    """
    bsc_api_key = "P8CHB9K1WSKYQXJ7BBDBPWZGER9U33DNDN"
    coinmarketcap_api_key = "baefec12-bbb8-4e7e-845e-24bd574d0cdc"
    contract_address = "0x1bdd3Cf7F79cfB8EdbB955f20ad99211551BA275"
    wallet_address = "0x60270bF99480FfDC71f2453A38117DA2ED7a5c77"
    decimal_places = 18

    bnbx_balance_smallest_decimal = get_token_balance(bsc_api_key, contract_address, wallet_address)
    bnbx_balance_normal_decimal = smallest_decimal_to_normal(int(bnbx_balance_smallest_decimal),\
                                                              decimal_places)
    bnbx_balance_normal_decimal_truncated = truncate_to_range(bnbx_balance_normal_decimal,\
                                                              min_value=1e-8, \
                                                                max_value=1000000000000)

    if bnbx_balance_normal_decimal_truncated is not None:
        print(f"BNBX残高: {bnbx_balance_normal_decimal_truncated}")
        jpy_amount = convert_to_jpy(coinmarketcap_api_key,\
                                     bnbx_balance_normal_decimal_truncated,\
                                        "BNBX")
        if jpy_amount is not None:
            print(f"JPY残高: {jpy_amount} JPY")
            return jpy_amount
        else:
            print("JPYへの変換ができませんでした。")
    else:
        print("BNBX残高が取得できませんでした。")

if __name__ == "__main__":
    get_bnbx_balance()
