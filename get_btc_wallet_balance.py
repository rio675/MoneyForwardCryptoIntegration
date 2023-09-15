"""module providing a btc wallet balance getter"""
import requests
from requests import Session
from bs4 import BeautifulSoup

def get_token_balance():
    """
    a function to get btc wallet balance from xpub public key
    """
    # BTC xpub wallet balanceのURL
    # Ledger内のsegwitアドレスの残高取得の良いAPI無し
    # xpubから取得できる良いAPIも無かったのでスクレイピングで暫定対応。レスポンス遅い、後でAPI再捜索。
    url = "https://www.blockchain.com/explorer/assets/btc/"\
        "xpub/xpub6BhqNhL28xrrRXSK6SHzLMob3EppmXNFaUmYJxHDsd"\
            "dVwLdQW2VZ3rprrJ8TSbqe7QmSzBZWAY8G9qq9Stzz3fEhr3fR7zfAtGXhLuBbtQy"

    # Specify a timeout value in seconds (e.g., 10 seconds)
    timeout_seconds = 10

    # HTTP GETリクエストを送信してHTMLを取得
    response = requests.get(url, timeout=timeout_seconds)
    html = response.text

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html, 'html.parser')

    # 特定の要素を抽出
    element = soup.find('div', class_='sc-242e2fca-9 ggNVeI')

    # 要素のテキストを抽出
    if element:
        text = element.get_text(strip=True)

        # BTCの文字列を削除
        text_without_btc = text.replace("BTC", "")
        print(text_without_btc)

        return text_without_btc
    else:
        print("要素が見つかりませんでした")

def convert_to_jpy(coinmarketcap_api_key, amount, symbol):
    """
    a function to convert btc to jpy with the current exchange rate
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

    # Specify a timeout value in seconds (e.g., 10 seconds)
    timeout_seconds = 10

    session = Session()
    session.headers.update(headers)
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

def get_btc_balance():
    """
    a function to get btc wallet balance in JPY
    """
    coinmarketcap_api_key = "baefec12-bbb8-4e7e-845e-24bd574d0cdc"

    #2.5はbybitアカウント分ハードコード。earn中のBTCバランス取得するAPI無い為。
    btc_balance_truncated = str(float(get_token_balance()) + 2.50777)

    if btc_balance_truncated  is not None:
        print(f"BTC残高: {btc_balance_truncated }")
        jpy_amount = convert_to_jpy(coinmarketcap_api_key, btc_balance_truncated, "BTC")
        if jpy_amount is not None:
            print(f"JPY残高: {jpy_amount} JPY")
            return jpy_amount
        else:
            print("JPYへの変換ができませんでした。")
            print(jpy_amount)
    else:
        print("BTC残高が取得できませんでした。")

if __name__ == "__main__":
    get_btc_balance()
