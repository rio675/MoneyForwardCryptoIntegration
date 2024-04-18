"""module providing a steth wallet balance getter"""
import requests
import time

from conversion_helpers import convert_to_jpy, smallest_decimal_to_normal, truncate_to_range

def get_token_balance(etherscan_api_key, contract_address, wallet_address, max_retries=3, retry_delay=1):
    """
    a function to get steth wallet balance from address with retry
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

    # リトライ回数と遅延時間の設定
    max_retries = 5
    retry_delay = 60

    for i in range(max_retries + 1):
        try:
            # APIリクエストの送信
            response = requests.get(url, params=params, timeout=timeout_seconds)

            # レスポンスのJSONデータを取得
            data = response.json()

            # トークン残高を取得
            token_balance = data.get("result")

            if token_balance is not None:
                return token_balance
            else:
                print("トークン残高が見つかりませんでした。")
        except requests.exceptions.RequestException as error:
            print(f"APIリクエストエラー: {error}")
            time.sleep(retry_delay)
        except ValueError as error:
            print(f"JSONデータの解析エラー: {error}")
            time.sleep(retry_delay)

    if i == max_retries:
        print(f"最大リトライ回数に達しました。")
        return None

def get_steth_balance():
    """
    a function to get steth wallet balance in JPY
    """
    etherscan_api_key = "8G7NJ255KV1W4M9P5IIUN7AWHIZDSQU9UD"
    contract_address = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
    wallet_address = "STETH_WALLET_ADDRESS"
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
