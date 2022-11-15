#selenuim関連のモジュールインポート文
#selenuim-related module import statement
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import datetime
import time
import sys

_URL = 'https://app.highlow.com/quick-demo'
# _URL_QUIC_DEMO = 'https://sushida.net/play.html'

options = webdriver.ChromeOptions()
# ヘッドレス化
# options.add_argument('--headless')
# UAをChromeに偽装
# options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')

try:
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    # driver_wait = WebDriverWait(driver=driver, timeout=60)
    #driver.implicitly_wait(60)
    driver.set_window_size(1920, 1080)
except Exception as e:
    print('Driver Init Error')
    raise

callback = []
#callback.append(entry())

def entry():
    print('entry()')

    driver.get(_URL)
    time.sleep(10)

    driver.maximize_window()
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(1)

    #ポップアップの削除
    driver.find_element(By.XPATH,'/html/body/main/div/div[16]/div/div[1]').click()
    time.sleep(1)

    # 金額の入力
    input_price = driver.find_element(By.CSS_SELECTOR,'input[class^="MoneyInputField_amount"]')
    time.sleep(1)
    input_price.send_keys('200000')
    time.sleep(1)

    #ワンクリックの有効化
    ocb = driver.find_element(By.CSS_SELECTOR,"div[class^='TradePanel_footer']")
    time.sleep(1)
    ocb.click()
    time.sleep(1)

    #highボタンのクリック
    high_btn = driver.find_element(By.CSS_SELECTOR,"div[id^='TradePanel_oneClickHighButton']")
    time.sleep(1)
    high_btn.click()

    # 待機
    for i in range(40):
        print(i)
        time.sleep(1)

    #スクリーンショット
    driver.save_screenshot('screenshot.png')
    sys.exit()

def main():
    try:
        entry()

    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    main()