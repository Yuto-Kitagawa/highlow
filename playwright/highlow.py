# Playwrightモジュール
from playwright.sync_api import sync_playwright

# 時間操作モジュール
import time
import datetime
# エラー処理に必要なモジュール
import sys

# ハイローのID
id = ""
# ハイローのパスワード
password = ""

# エントリー金額
entry_price = 1000

ticker = "USD/JPY"
duration = "3分"

# エントリー時間
hour = 19
minute = 50
second = 0

# 曜日を取得
today = datetime.date.today()
# 0:月～6:日
today_weekdaty = today.weekday()
target_weekday = [0,1,2,3,4]


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # ブラウザーを開く
    page = context.new_page()
    
    try:
        #===========================================
        # ログイン処理
        #===========================================
        page.set_default_navigation_timeout(0)

        # ログインページに移動
        page.goto("https://app.highlow.com/login")

        # 読み込みを待機
        page.wait_for_load_state("networkidle")

        # IDを入力
        page.locator("input[id^=login-username]").focus()
        page.locator("input[id^=login-username]").fill(id)
        time.sleep(1)

        # パスワードを入力
        page.locator("input[id^=login-password]").focus()
        page.locator("input[id^=login-password]").fill(password)
        time.sleep(1)

        # ログインボタンをクリック
        page.locator("div[id^=login-submit-button]").click()

        # 読み込みを待機
        page.wait_for_load_state("load")
        for i in range(20):
            time.sleep(1)
            print(i)

        #===========================================
        # エントリー準備
        #===========================================

        # 1クリック注文をチェック
        if(page.locator("input[data-test='one-click-enabled-button']").is_checked() is True):
            page.locator("div[class^=TradePanel_footer]").click()
            
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
            print(option_ticker.text_content())
            # オプション時間を取得
            option_duration = option.locator("span[class^=OptionItem_duration]")
            # 取得したオプションがUSD/JPYの30秒の場合クリック
            if option_ticker.text_content() == ticker and option_duration.text_content() == duration:
                option.click()
                break

        # 5秒待機
        time.sleep(5)

        # エントリー金額を入力
        page.locator("input[data-test='trade-amount']").fill(str(entry_price))

        # HIGHボタンを取得
        high_trade_button = page.locator("div[id^=HIGH_TRADE_BUTTON]")
        # LOWボタンを取得
        low_trade_button = page.locator("div[id^=LOW_TRADE_BUTTON]")

        # 現在時刻とエントリー時刻を取得
        today = datetime.datetime.now()
        tartget_d = datetime.datetime(today.year, today.month, today.day, hour, minute, second, 0)
        target_time = int(time.mktime(tartget_d.timetuple()))
        now_time = int(time.mktime(today.timetuple()))

        #===========================================
        # 待機＆エントリー
        #===========================================
        # エントリー時間まで待機
        waiting_time = target_time - now_time
        if waiting_time > 0:
            time.sleep(waiting_time)
        else:
            # エントリー時刻を過ぎていた場合終了する
            print("エントリー時刻を超過しています。")
            return

        # LOWボタンクリック
        high_trade_button.click()
        
        # 90秒待機する
        time.sleep(90)
    # エラー出力
    except Exception as e:
        print(str(e))
        print("エラーが発生しました")

    # 終了処理
    finally:
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
        if id == "":
            print("IDが未設定です。")
        elif password == "":
            print("パスワードが未設定です。")
        elif entry_price < 1000:
            print("エントリー金額が1,000円未満です")
        elif ticker == "":
            print("通貨ペアが未設定です")
        elif ticker == "":
            print("オプションの期間が未設定です")
        else:
            # 自動エントリーを実行する
            run(playwright)
    sys.exit()