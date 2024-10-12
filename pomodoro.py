import ctypes
import time
from pystray import icon,Menu,MenuItem
from PIL import Image;

def show_notification(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def start_pomodoro():
    pomodoro_duration = 25 * 60  # 25分
    break_duration = 5 * 60  # 5分
    sessions = 4

    for session in range(sessions):
        print(f"セッション {session + 1} 開始: 25分")
        show_notification("ポモドーロタイマー", "作業時間スタート！集中しましょう。")
        time.sleep(pomodoro_duration)

        if session < sessions - 1:
            print("休憩時間: 5分")
            show_notification("ポモドーロタイマー", "休憩時間です。リラックスしてください！")
            time.sleep(break_duration)
        else:
            print("全てのセッションが完了しました！")
            show_notification("ポモドーロタイマー", "全てのセッションが完了しました！")

# タスクトレー作成
def tasktray_create():
    try:
        global icon
        item=[]
        options_map = {'Test': lambda: tasktray_test(),'Quit': lambda: tasktray_abort()}
 
        for option,callback in options_map.items():
            item.append( MenuItem(option,callback,default=True if option == 'Show' else False ) )
            
        menu = Menu(*item)

        image = Image.open("app.ico")
        icon = Icon("name",image,"My System Tray Icon", menu)
        icon.run()
    finally:
        tasktray_abort()

def tasktray_test():
    print("TaskTray Test")
    
def tasktray_abort():
    global icon
    if icon != 0:
        icon.stop()

if __name__ == "__main__":
    start_pomodoro()

