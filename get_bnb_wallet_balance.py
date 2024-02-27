"""module providing a bnbx wallet balance getter"""
import requests

from conversion_helpers import convert_to_jpy, smallest_decimal_to_normal, truncate_to_range

def get_bnb_balance():
    """
    a function to get bnbx wallet balance in JPY
    """
    coinmarketcap_api_key = "baefec12-bbb8-4e7e-845e-24bd574d0cdc"

    # hardcoded wallet balance. The balance will be updated from github secret
    bnb_balance_normal_decimal_truncated = str('BNB_WALLET_BALANCE')

    if bnb_balance_normal_decimal_truncated is not None:
        print(f"BNB残高: {bnb_balance_normal_decimal_truncated}")
        jpy_amount = convert_to_jpy(coinmarketcap_api_key,\
                                     bnb_balance_normal_decimal_truncated,\
                                        "BNB")
        if jpy_amount is not None:
            print(f"JPY残高: {jpy_amount} JPY")
            return jpy_amount
        else:
            print("JPYへの変換ができませんでした。")
    else:
        print("BNB残高が取得できませんでした。")

if __name__ == "__main__":
    get_bnb_balance()
