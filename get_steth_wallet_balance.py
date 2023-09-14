"""module providing a steth wallet balance getter"""
import requests
from requests import Session

def get_token_balance(etherscan_api_key, contract_address, wallet_address):
    """
    a function to get steth wallet balance from address
    """
    # Etherscan APIのエンドポイント
    url = "https://api.etherscan.io/api"

    # パラメーター設定
    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": wallet_address,
        "tag": "latest",
        "apikey": etherscan_api_key  # ここに実際のAPIキーを入力してください
    }

    # Specify a timeout value in seconds (e.g., 10 seconds)
    timeout_seconds = 10

    try:
        # APIリクエストの送信
        response = requests.get(url, params=params, timeout=timeout_seconds)

        # レスポンスのJSONデータを取得
        data = response.json()

        # トークン残高を取得
        token_balance = data.get("result")

        if token_balance is not None:
            print(f"トークン残高: {token_balance}")
            return token_balance
        else:
            print("トークン残高が見つかりませんでした。")
    except requests.exceptions.RequestException as error:
        print(f"APIリクエストエラー: {error}")
    except ValueError as error:
        print(f"JSONデータの解析エラー: {error}")

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

    response = requests.get(api_url, params=params, headers=headers, timeout=timeout_seconds)

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

def get_steth_balance():
    """
    a function to get steth wallet balance in JPY
    """
    etherscan_api_key = "8G7NJ255KV1W4M9P5IIUN7AWHIZDSQU9UD"
    contract_address = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
    wallet_address = "0x60270bF99480FfDC71f2453A38117DA2ED7a5c77"
    coinmarketcap_api_key = "baefec12-bbb8-4e7e-845e-24bd574d0cdc"
    decimal_places = 18

    steth_balance_smallest_decimal = get_token_balance(etherscan_api_key,\
                                                        contract_address, wallet_address)
    steth_balance_normal_decimal = smallest_decimal_to_normal(int(steth_balance_smallest_decimal),\
                                                               decimal_places)
    steth_balance_normal_decimal_truncated = truncate_to_range(steth_balance_normal_decimal,\
                                                                min_value=1e-8,\
                                                                      max_value=1000000000000)

    if steth_balance_normal_decimal_truncated is not None:
        print(f"STETH残高: {steth_balance_normal_decimal_truncated}")
        jpy_amount = convert_to_jpy(coinmarketcap_api_key,\
                                     steth_balance_normal_decimal_truncated, "STETH")
        if jpy_amount is not None:
            print(f"JPY残高: {jpy_amount} JPY")
            return jpy_amount
        else:
            print("JPYへの変換ができませんでした。")
    else:
        print("STETH残高が取得できませんでした。")

if __name__ == "__main__":
    get_steth_balance()
