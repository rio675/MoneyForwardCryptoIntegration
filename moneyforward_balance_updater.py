# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

url = "" #銀行のURL
user = "" #自分のアカウント
password = "" #自分のパスワード

try:
    # Microsoft Edgeを起動

    driver = webdriver.Edge()
    driver.implicitly_wait(10)  # wait

    #マネーフォワードの銀行ページに遷移
    driver.get(url)

    wait = WebDriverWait(driver, 10)

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
    button = driver.find_element(By.CLASS_NAME, "btn.btn-success")
    button.click()

    driver.implicitly_wait(3)   #wait

    #残高修正入力
    elem = driver.find_element(By.ID, "rollover_info_value")
    elem.clear()
    elem.send_keys("1111")

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