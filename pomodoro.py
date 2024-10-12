import time
import ctypes
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
from win10toast import ToastNotifier  # win10toast を使って Windows の通知を実現

# タイマーの状態フラグ
is_running = False

# 通知を表示するためのオブジェクト
toaster = ToastNotifier()
# TODO: トースト通知を行う
# def show_notification(title, message):
#     # win10toast を使用してシステム通知を表示
#     toaster.show_toast(
#         title,
#         message,
#         duration=10,  # 通知が表示される秒数
#         threaded=True  # 別スレッドで通知を表示する
#     )

# 通知オブジェクト作成
def show_notification(title, message):
    # メインスレッドで MessageBoxW を呼び出す
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

# ###################################
# タイマー処理                       #
# ###################################

# タイマー起動メソッド
def start_pomodoro_thread():
    # ポモドーロタイマーを別スレッドで開始
    threading.Thread(target=start_pomodoro, daemon=False).start()

def start_pomodoro():
    global is_running
    is_running = True
    update_menu()  # メニューを更新して開始ボタンを無効化

    pomodoro_duration = 25 * 60  # 25分
    break_duration = 5 * 60      # 5分
    sessions = 4                 # 1セッション回数

    for session in range(sessions):
        if not is_running:  # キャンセルされた場合に終了
            break
        # 作業セッション処理
        print(f"セッション {session + 1} 開始: 25分")
        show_notification("ポモドーロタイマー", "作業時間スタート！集中しましょう。")
        time.sleep(pomodoro_duration)

        if session < sessions - 1:
            # 休憩セッション処理
            print("休憩時間: 5分")
            show_notification("ポモドーロタイマー", "休憩時間です。リラックスしてください！")
            time.sleep(break_duration)
        else:
            print("全てのセッションが完了しました！")
            show_notification("ポモドーロタイマー", "全てのセッションが完了しました！")

    is_running = False
    update_menu()  # メニューを更新して終了ボタンを無効化

# ポモドーロタイマー停止メソッド
def stop_pomodoro():
    global is_running
    is_running = False
    update_menu()
    # メインスレッドで MessageBoxW を呼び出す
    # show_notification("ポモドーロタイマー", "セッションを終了します！お疲れさまでした。")

# ###################################
# システムトレー作成                  #
# ###################################

# システムトレイ作成スレッド作成
def start_systemtray_thread():
    # システムトレイを別スレッドで起動
    tasktray_thread = threading.Thread(target=systemtray_create)
    tasktray_thread.daemon = False  # メインスレッド終了時に自動終了
    tasktray_thread.start()

# システムトレイ作成メソッド
def systemtray_create():
    global Icon
    # アイコン作成
    image = Image.open("./tomato.ico")
    Icon = Icon("name", image, "ポモドーロタイマー")
    update_menu()
    Icon.run()

# メニューアイテム更新メソッド
def update_menu():
    global Icon, is_running
    # メニューアイテムを動的に作成
    menu_items = []
    if is_running:
        # タイマーが動いている場合、「開始」ボタンを無効にし、「終了」ボタンを有効にする
        menu_items.append(MenuItem("開始", lambda: None, enabled=False))
        menu_items.append(MenuItem("終了", stop_pomodoro, enabled=True))
    else:
        # タイマーが動いていない場合、「開始」ボタンを有効にし、「終了」ボタンを無効にする
        menu_items.append(MenuItem("開始", start_pomodoro_thread, enabled=True))
        menu_items.append(MenuItem("終了", lambda: None, enabled=False))

    # 新しいメニューを適用
    Icon.menu = Menu(*menu_items)

# メイン処理
if __name__ == "__main__":
    # タイマースレッド起動
    start_pomodoro_thread()
    # システムトレイ作成
    start_systemtray_thread()