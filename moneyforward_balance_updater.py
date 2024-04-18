"""module providing a lambda function to integrate crypto assets to MoneyForward."""
import time
from playwright.sync_api import sync_playwright

from get_bnb_wallet_balance import get_bnb_balance
from get_bnbx_wallet_balance import get_bnbx_balance
from get_btc_wallet_balance import get_btc_balance
from get_steth_wallet_balance import get_steth_balance
from get_pepe_wallet_balance import get_pepe_balance
from get_shib_wallet_balance import get_shib_balance

# pylint: disable=W0613
def lambda_handler(event, context):
    """
    メインのLambdaハンドラ関数
    """
    url = 'MONEYFORWARD_BANK_URL'
    user = 'MY_EMAIL_ADDRESS'
    password = 'MONEYFORWARD_PASSWORD'
    # Chromeをheadlessモードで起動
    with sync_playwright() as playwright:
        # Open a new browser context
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            #Change user agent 以下のようにuser_agentを偽造しないと、MoneyForwardのログイン画面が表示されないため。
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url)        
        login_to_moneyforward(page, user, password)
        update_moneyforward_balance(page)
        context.close()
        browser.close()

def login_to_moneyforward(page, user, password):
    """
    マネーフォワードにログインする関数
    """
    page.fill('#mfid_user\\[email\\]', user)
    # Click the submit button
    page.click('#submitto')
    page.wait_for_load_state('networkidle')
    # Fill in the password field
    page.fill('#mfid_user\\[password\\]', password) 
    # Click the submit (sign in) button
    page.click('#submitto')
    page.wait_for_load_state('networkidle')
    return page

def delete_all_cash_deposit(page):
    page.wait_for_load_state('networkidle')
    # Click all delete buttons(削除ボタンがなくなるまで削除ボタンをクリックし続ける)
    while True:
        # Handle dialog (popup)　表示されるダイアログを自動的に承認（OKボタンを押す）する。
        page.once("dialog", lambda dialog: dialog.accept())
        # Find all delete buttons within the specified table
        delete_buttons = page.query_selector_all('.table.table-bordered.table-depo .btn-asset-action[data-method="delete"]')
        # If no more delete buttons, break the loop
        if not delete_buttons:
            break
        # Click the first delete button
        delete_buttons[0].click()
        # Wait for navigation (optional, depending on the page)
        page.wait_for_load_state('networkidle')

def create_asset_in_mf(page, asset_type, asset_name, market_value, max_retries=5, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            page.wait_for_load_state('networkidle')
            page.once("dialog", lambda dialog: dialog.accept())
            page.wait_for_load_state('networkidle')
            # マネーフォワードの残高を新規作成する関数
            page.get_by_role("button", name="手入力で資産を追加").click()
            page.get_by_role("combobox", name="資産の種類").select_option(str(asset_type))
            page.get_by_label("資産の名称").fill(str(asset_name)[:20])
            page.get_by_label("現在の価値").fill(str(market_value)[:12])
            page.get_by_role("button", name="この内容で登録する").click()
            page.wait_for_timeout(2000)
            page.wait_for_load_state('networkidle')
            return True
        except Exception as e:
            retries += 1
            print(f"Error occurred: {e}. Retrying ({retries}/{max_retries})...")
            time.sleep(retry_interval)  # 一定時間待機してから再試行   
    # 最大再試行回数に達した場合
    print(f"Maximum retries ({max_retries}) exceeded. Failed to create asset.")
    return False

def update_asset_value(page, asset_name, market_value):
    # シンボルに対応するボタンのセレクターを作成
    button_selector = f"//td[text()='{asset_name}']/..//a[@data-toggle='modal']"
    if button_selector:
        # ボタンをクリック
        page.query_selector(button_selector).click()
        # 新しい価値を入力
        page.get_by_role("row", name=asset_name).locator("#user_asset_det_value").fill(str(market_value)[:12])
        page.get_by_role("button", name="この内容で登録する").click()
        page.wait_for_timeout(2000)
        page.wait_for_load_state('networkidle')
    else:
        #前の入力項目を全削除
        #delete_all_cash_deposit(page)
        #入力済み仮想通貨資産が無い為、資産額を新規入力
        #66とはまMF内の資産の種類の’暗号資産’のこと
        create_asset_in_mf(page, 66, 'BTC', get_btc_balance())
        create_asset_in_mf(page, 66, 'BNB', get_bnb_balance())
        create_asset_in_mf(page, 66, 'STETH', get_steth_balance())
        create_asset_in_mf(page, 66, 'PEPE', get_pepe_balance())
        create_asset_in_mf(page, 66, 'SHIB', get_shib_balance())
    return True

def update_moneyforward_balance(page):  
    update_asset_value(page, 'BTC',   get_btc_balance())
    update_asset_value(page, 'BNB',   get_bnb_balance())
    update_asset_value(page, 'STETH', get_steth_balance())
    update_asset_value(page, 'PEPE',  get_pepe_balance())
    update_asset_value(page, 'SHIB',  get_shib_balance())
    return page

if __name__ == "__main__":
    event = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
    context = {
        "function_name": "my_lambda_function",
        "runtime": "python3.9",
        "memory_limit_in_mb": 128,
        "timeout": 30,
        "log_group_name": "/aws/lambda/my_lambda_function",
        "request_id": "1234567890"
    }
    lambda_handler(event, context)
