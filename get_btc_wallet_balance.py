"""module providing a btc wallet balance getter"""
import requests

from bs4 import BeautifulSoup
from conversion_helpers import convert_to_jpy

def get_token_balance():
    """
    a function to get btc wallet balance from xpub public key
    """
    # BTC xpub wallet balanceのURL
    # Ledger内のsegwitアドレスの残高取得の良いAPI無し
    # xpubから取得できる良いAPIも無かったのでスクレイピングで暫定対応。レスポンス遅い、後でAPI再捜索。
    url = 'BTC_WALLET_BALANCE_URL'

    # Specify a timeout value in seconds (e.g., 10 seconds)
    timeout_seconds = 20

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

def get_btc_balance():
    """
    a function to get btc wallet balance in JPY
    """
    coinmarketcap_api_key = "baefec12-bbb8-4e7e-845e-24bd574d0cdc"

    #bybit＋NEXOアカウント分ハードコード。bybit earn中のBTCバランス取得するAPI & NEXO API無い為。
    btc_balance_truncated = str(float(get_token_balance()) + float('BTC_WALLET_BALANCE'))

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
