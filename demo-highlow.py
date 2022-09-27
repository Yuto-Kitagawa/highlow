"""
pip install playwright
python -m playwright install

デモバージョンは、ログイン処理がいらないのでID・password・時間指定を削除しています。
"""

# playwrightモジュール
from playwright.sync_api import sync_playwright
# 時間操作モジュール
import time
import datetime
import sys

"""エントリー金額"""
entry_price = 10000

#選択するオプション
ticker = "USD/JPY"
duration = "30秒"

#曜日を取得
today = datetime.date.today()
today_weekdaty = today.weekday()
#月0 火1 水2 木3 金4 土5 日6
target_weekday = [0,1,2,3,4]


def run(playwright):
    # ブラウザを操作する設定
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        page.set_default_navigation_timeout(0)

        # URLに移動
        page.goto("https://app.highlow.com/quick-demo")

        # 待機
        page.wait_for_load_state("networkidle")

        time.sleep(5)
        
        # 口座残高の取得
        valanceValue_default = page.locator("span[id^=balanceValue]").text_content()
        valanceValue_str = valanceValue_default[1:]
        valanceValue = valanceValue_str.replace(",","")

        # 口座残高が1000円以下の時のエラー処理
        if int(valanceValue) < 1000:
            print("口座残高が1000円以下なので実行がキャンセルされました。")
            return
        # エントリー分の残高がない。
        elif int(valanceValue) < entry_price:
            print("口座残高にエントリー分の残高がありません")
            return

        # オプション一覧を取得する
        options = page.locator("div[class^=OptionItem_container]")

        # 対象のオプションを選ぶ
        options_count = options.count()
        for i in range(options_count):
            option = options.nth(i)
            # 通貨ペア取得
            option_ticker = option.locator("span[class^=OptionItem_ticker]")
            # オプション時間を取得
            option_duration = option.locator("span[class^=OptionItem_duration]")
            # 取得したオプションがUSD/JPYの30秒の場合クリック
            if option_ticker.text_content() == ticker and option_duration.text_content() == duration:
                option.click()
                break
            
        time.sleep(2)

        # エントリー金額をフォームに入力
        page.locator("input[data-test='trade-amount']").fill(str(entry_price))

        time.sleep(1)

        # 1クリック注文をチェック
        if(page.locator("input[data-test='one-click-enabled-button']").is_checked() is False):
            page.locator("div[class^=TradePanel_footer]").click()

        # HIGHボタンを取得
        high_trade_button = page.locator("div[id^=TradePanel_oneClickHighButton]")
        # LOWボタンを取得
        low_trade_button = page.locator("div[id^=TradePanel_oneClickLowButton]")

        time.sleep(5)

        # lowボタンエントリー
        low_trade_button.click()

    # エラー出力
    except Exception as e:
        print(e)
    
    # 終了処理
    finally:
        time.sleep(35)
        # ブラウザを閉じる
        page.close()
        context.close()
        browser.close()
        

#===========================================
# メイン関数実行
#===========================================
with sync_playwright() as playwright:
    # 平日のみ実行する。
    if today_weekdaty in target_weekday:
        # 入力項目チェック
        if entry_price < 1000:
            print("エントリー金額が1,000円未満です")
        elif ticker == "":
            print("通貨ペアが未設定です")
        elif ticker == "":
            print("オプションの期間が未設定です")
        else:
            # 自動エントリーを実行する
            run(playwright)
    sys.exit()