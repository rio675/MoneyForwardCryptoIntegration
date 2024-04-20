"""module providing a pepe wallet balance getter"""
from conversion_helpers import convert_to_jpy

def get_pepe_balance():
    """
    a function to get pepe wallet balance in JPY
    """
    coinmarketcap_api_key = "baefec12-bbb8-4e7e-845e-24bd574d0cdc"

    # hardcoded wallet balance. The balance will be updated from github secret
    pepe_balance_normal_decimal_truncated = str('PEPE_WALLET_BALANCE')

    if pepe_balance_normal_decimal_truncated is not None:
        print(f"PEPE残高: {pepe_balance_normal_decimal_truncated}")
        jpy_amount = convert_to_jpy(coinmarketcap_api_key,\
                                     pepe_balance_normal_decimal_truncated,\
                                        "pepe")
        if jpy_amount is not None:
            print(f"JPY残高: {jpy_amount} JPY")
            return jpy_amount
        else:
            print("JPYへの変換ができませんでした。")
    else:
        print("PEPE残高が取得できませんでした。")

if __name__ == "__main__":
    get_pepe_balance()
