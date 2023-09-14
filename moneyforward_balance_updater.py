"""module providing a lambda function to integrate crypto assets to MoneyForward."""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from get_bnbx_wallet_balance import get_bnbx_balance
from get_btc_wallet_balance import get_btc_balance
from get_steth_wallet_balance import get_steth_balance

# pylint: disable=W0613
def lambda_handler(event, context):
    """
    a main lambda function to input balance to money forward by selenium
    """

    url = 'MONEYFORWARD_BANK_URL'#MoneyForwardの更新したい口座のURL
    user= 'MY_EMAIL_ADDRESS'#MoneyForwardの自分のアカウント
    password = 'MONEYFORWARD_PASSWORD'#MoneyForwardの自分のパスワード

    try:
        # Chromeをheadlessモードで起動
        driver_path ='/opt/headless/chromedriver'
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/headless/headless-chromium"
        # ヘッドレスモードでChromeを起動
        options.add_argument("--headless")
        # セキュリティ設定の一部を無効化
        options.add_argument("--no-sandbox")
        # シングルプロセスモードでChromeを起動
        options.add_argument('--single-process')
        # /dev/shmの使用を無効化
        options.add_argument('--disable-dev-shm-usage')
        # WebページによるHeadless検出回避の為のダミーデータ
        options.add_argument("user-agent=Mozilla/5.0\
                             (Windows NT 10.0; Win64; x64)\
                              AppleWebKit/537.36 (KHTML, like Gecko)\
                              Chrome/58.0.3029.110 Safari/537.36")
        # pylint: disable=E1123
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        driver.implicitly_wait(10)  # wait

        #マネーフォワードの銀行ページに遷移
        driver.get(url)

        WebDriverWait(driver, 10)

        #アカウント入力
        elem = driver.find_element(By.ID, "mfid_user[email]")
        elem.clear()
        elem.send_keys(user)

        #ログインボタンクリック
        button = driver.find_element(By.ID, "submitto")
        button.click()

        driver.implicitly_wait(3)   #wait

        #パスワード入力
        elem = driver.find_element(By.ID, "mfid_user[password]")
        elem.clear()
        elem.send_keys(password)

        #ログインボタンクリック
        button = driver.find_element(By.ID, "submitto")
        button.click()

        driver.implicitly_wait(3)   #wait

        #残高修正ボタンクリック
        button = driver.find_element(By.LINK_TEXT, "残高修正")
        button.click()

        driver.implicitly_wait(3)   #wait

        #残高合計金額を計算
        total_balance = calculate_sum( get_bnbx_balance(), get_btc_balance(), get_steth_balance() )

        #残高修正入力
        elem = driver.find_element(By.ID, "rollover_info_value")
        elem.clear()
        elem.send_keys(total_balance)

        driver.implicitly_wait(3)   #wait

        # form要素を特定（id属性を使用）
        form_element = driver.find_element(By.ID, 'rollover_form')

        # form要素内の全ての<input>要素を取得
        input_elements = form_element.find_elements(By.TAG_NAME, 'input')

        # <input>要素の中からname属性が"commit"であるものを特定
        commit_button = None
        for input_element in input_elements:
            if input_element.get_attribute('name') == 'commit':
                commit_button = input_element
                break

        #この内容で登録するボタンをクリック
        commit_button.click()

        #確認用wait
        time.sleep(10)

    finally:
        print("End")
        driver.quit()

def calculate_sum(*balances):
    """
    a sum function to calculate sum of the balances
    """
    return sum(balances)
