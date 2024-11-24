from src.console import CustomPrint
console = CustomPrint()
import textwrap

from src.setting import env, config
from src.log import Logger
logger = Logger()

import re
# 色を取り除く関数
def remove_color(text: str) -> str:
    # ANSIエスケープシーケンス（色コード）を取り除く正規表現
    return re.sub(r'\x1b\[[0-9;]*m', '', text)
from src.colors import ColorManager  # ColorManager のインポート
color_manager = ColorManager(config().get("colors", {}))
color_reset = color_manager.get_color('reset', '')

def get_color(key: str):
    return color_manager.get_color(key,'')

import scratchattach as sa
from scratchattach import Encoding

from time import time

# Scratch クラウド変数 ----------------------------------------------
username = env("USERNAME")
password = env("PASSWORD")
project_id = config().get("project_id")

session = sa.login(username, password)  # Log in to Scratch
cloud = session.connect_scratch_cloud(project_id)  # Connect Scratch's cloud

def post_cloud_req():
    value = time()
    cloud.set_var("hack", value)

# 実行 / 終了 ----------------------------------------------
from threading import Event, Thread
from pynput import keyboard
from time import sleep
import signal

stop_flag = Event()

def cleanup():
    """終了時のクリーンアップ処理"""
    console.info("クリーンアップ処理中... イベント監視を終了します。")
    stop_flag.set()
    exit(0)

def signal_handler(sig, frame):
    """シグナルハンドラ"""
    console.info(f"シグナル {sig} を検知しました。")
    cleanup()

# シグナルをハンドルする
signal.signal(signal.SIGINT, signal_handler)  # Ctrl + C
signal.signal(signal.SIGTERM, signal_handler)  # プロセス終了

def monitor_exit():
    def on_press(key):
        try:
            if key.char == 'q':  # 'q' キーが押されたら
                console.debug(f"{color_manager.get_color('debug','')}ユーザーが 'q' を押しました。コードを終了します...{color_reset}")
                stop_flag.set()  # フラグをセットして終了を通知
                return False  # リスナーを終了
        except AttributeError:
            pass
        sleep(0.1)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def start_event_monitor():
    """イベント監視スレッド"""
    try:
        while not stop_flag.is_set():
            post_cloud_req()  # Scratchクラウド変数に値をポストする
            sleep(0.1)  # 1秒ごとにポストする
    except Exception as e:
        console.error(f"エラー発生: {e}")
    finally:
        console.info("コードを終了します。")

# 実行開始
if __name__ == "__main__":
    print(textwrap.dedent(f"""
=======================================

    Scratch Cloud Event Monitor / hack
    ___________________________
    
    起動構成:
    - ユーザー名: {color_manager.get_color('info', '')}{username}{color_reset}
    - プロジェクトID: {color_manager.get_color('info', '')}{project_id}{color_reset}

=======================================
"""))
    # ログファイルを生成するか尋ねる
    print("ログファイルを作成して、イベントを記録することができます。")
    enable_logging = input("ログをファイルに出力しますか？ (y/n): ").strip().lower()
    if enable_logging == "y":
        logger.setup_logging()
    else:
        print(f"{color_manager.get_color('warning', '')}ログファイル出力は無効です。{color_reset}")

    print("準備ができました。")
    print("スクリプトを開始するには、Enterキーを押してください。")
    console.info("スクリプトを終了するには、'q' または 'Ctrl + C' キーを押してください。'SIGTERM' でも終了できます。")

    # 監視の開始前にEnterキーを待機
    input("\nEnterを押すとスクリプトを開始します...")

    # イベント監視スレッドを開始
    monitor_thread = Thread(target=start_event_monitor, daemon=True)
    monitor_thread.start()

    # メインスレッドで待機（強制終了まで）
    try:
        # キーボード入力監視スレッドを開始
        exit_thread = Thread(target=monitor_exit, daemon=True)
        exit_thread.start()

        while not stop_flag.is_set():
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
        monitor_thread.join()
        console.info("プログラムを正常に終了しました。")
        exit(0)