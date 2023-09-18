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
    メインのLambdaハンドラ関数
    """
    try:
        url = 'MONEYFORWARD_BANK_URL'
        user = 'MY_EMAIL_ADDRESS'
        password = 'MONEYFORWARD_PASSWORD'

        driver = setup_browser()
        login_to_moneyforward(driver, url, user, password)
        update_moneyforward_balance(driver)
    finally:
        driver.quit()
        print("End")

def setup_browser():
    """
    ブラウザのセットアップを行う関数
    """
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
    driver.implicitly_wait(10)
    return driver

def login_to_moneyforward(driver, url, user, password):
    """
    マネーフォワードにログインする関数
    """

    driver.get(url)
    WebDriverWait(driver, 10)

    elem = driver.find_element(By.ID, "mfid_user[email]")
    elem.clear()
    elem.send_keys(user)

    button = driver.find_element(By.ID, "submitto")
    button.click()

    driver.implicitly_wait(3)

    elem = driver.find_element(By.ID, "mfid_user[password]")
    elem.clear()
    elem.send_keys(password)

    button = driver.find_element(By.ID, "submitto")
    button.click()

    driver.implicitly_wait(3)

    button = driver.find_element(By.LINK_TEXT, "残高修正")
    button.click()

    driver.implicitly_wait(3)

def update_moneyforward_balance(driver):
    """
    マネーフォワードの残高を更新する関数
    """
    total_balance = calculate_sum(get_bnbx_balance(), get_btc_balance(), get_steth_balance())

    elem = driver.find_element(By.ID, "rollover_info_value")
    elem.clear()
    elem.send_keys(total_balance)

    driver.implicitly_wait(3)

    form_element = driver.find_element(By.ID, 'rollover_form')
    input_elements = form_element.find_elements(By.TAG_NAME, 'input')

    commit_button = None
    for input_element in input_elements:
        if input_element.get_attribute('name') == 'commit':
            commit_button = input_element
            break

    commit_button.click()
    time.sleep(10)

def calculate_sum(*balances):
    """
    残高の合計を計算する関数
    """
    return sum(balances)
