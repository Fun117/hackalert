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

from src.hackalert import HackAlert
hackAlert = HackAlert()

# Scratch クラウド変数 ----------------------------------------------
username = env("USERNAME")
password = env("PASSWORD")
project_id = config().get("project_id")

session = sa.login(username, password)  # Log in to Scratch
cloud = session.connect_scratch_cloud(project_id)  # Connect Scratch's cloud
events = cloud.events()

# イベントハンドラー ----------------------------------------------
@events.event
def on_set(activity):  # Called when a cloud var is set
    hackAlert.alert_on_set(activity)

    color_config = config().get("logs", {}).get("on_set", {}).get("colors", "")
    var_color = get_color(color_config.get('var', 'none'))
    value_color = get_color(color_config.get('value', 'none'))
    timestamp_color = get_color(color_config.get('timestamp', 'none'))
    username_color = get_color(color_config.get('username', 'none'))
    decode_color = get_color(color_config.get('decode', 'none'))
    
    decode_value = Encoding.decode(int(activity.value))
    format_str = config().get("logs", {}).get("on_set", {}).get("format", "Variable <var> was set to the value <value> at <timestamp>")
    formatted_with_color = format_str.replace('<var>', f"{var_color}{activity.var}{color_reset}") \
        .replace('<value>', f"{value_color}{activity.value}{color_reset}") \
        .replace('<timestamp>', f"{timestamp_color}{activity.timestamp}{color_reset}") \
        .replace('<username>', f"{username_color}{activity.username}{color_reset}") \
        .replace('<decode>', f"{decode_color}{decode_value}{color_reset}")
    console.log(formatted_with_color)

    # 色なしで保存するために色コードを取り除く
    formatted_without_color = remove_color(formatted_with_color)
    logger.log_message(formatted_without_color)

@events.event
def on_del(activity):
    hackAlert.alert_on_del(activity)

    color_config = config().get("logs", {}).get("on_del", {}).get("colors", "")
    var_color = get_color(color_config.get('var', 'none'))
    user_color = get_color(color_config.get('user', 'none'))

    format_str = config().get("logs", {}).get("on_del", {}).get("format", "<user> deleted variable <var>")
    formatted_with_color = format_str.replace('<var>', f"{var_color}{activity.var}{color_reset}") \
        .replace('<user>', f"{user_color}{activity.user}{color_reset}")

    console.log(formatted_with_color)
    # 色なしで保存するために色コードを取り除く
    formatted_without_color = remove_color(formatted_with_color)
    logger.log_message(formatted_without_color)

@events.event
def on_create(activity):
    hackAlert.alert_on_create(activity)

    color_config = config().get("logs", {}).get("on_create", {}).get("colors", "")
    var_color = get_color(color_config.get('var', 'none'))
    user_color = get_color(color_config.get('user', 'none'))

    format_str = config().get("logs", {}).get("on_create", {}).get("format", "<user> created variable <var>")
    formatted_with_color = format_str.replace('<var>',  f"{var_color}{activity.var}{color_reset}") \
        .replace('<user>',  f"{user_color}{activity.user}{color_reset}")

    console.log(formatted_with_color)
    # 色なしで保存するために色コードを取り除く
    formatted_without_color = remove_color(formatted_with_color)
    logger.log_message(formatted_without_color)

@events.event  # Called when the event listener is ready
def on_ready():
    message = str(config().get("logs", {}).get("on_ready", {}).get("message", "Event listener ready!"))
    console.log(message)

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
                console.debug(f"{color_manager.get_color('debug','')}ユーザーが 'q' を押しました。イベント監視を終了します...{color_reset}")
                stop_flag.set()  # フラグをセットして終了を通知
                return False  # リスナーを終了
        except AttributeError:
            pass
        sleep(0.1)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# イベント監視スレッド
def start_event_listener():
    """Scratchイベント監視を開始"""
    try:
        events.start(thread=True, ignore_exceptions=True)  # スレッドモードで開始
        while not stop_flag.is_set():  # 停止フラグがセットされるまでループ
            sleep(0.1)  # CPU負荷を抑えるために少し待機
    except Exception as e:
        console.error(f"エラー: {e}")
    finally:
        console.info("イベント監視を終了しました")
        stop_flag.set()
        return False

def start_event_monitor():
    """イベント監視スレッド"""
    try:
        while not stop_flag.is_set():
            # ここでScratchのイベントを監視する処理を実装
            sleep(0.1)  # ダミー処理
    except Exception as e:
        console.error(f"エラー発生: {e}")
    finally:
        console.info("イベント監視を終了します。")

# 実行開始
if __name__ == "__main__":
    print(textwrap.dedent(f"""
=======================================

    Scratch Cloud Event Monitor
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
    print("イベントを監視するには、Enterキーを押してください。")
    console.info("監視を終了するには、'q' または 'Ctrl + C' キーを押してください。'SIGTERM' でも終了できます。")

    # 監視の開始前にEnterキーを待機
    input("\nEnterを押すと監視を開始します...")

    # イベント監視スレッドを開始
    monitor_thread = Thread(target=start_event_monitor, daemon=True)
    monitor_thread.start()

    # メインスレッドで待機（強制終了まで）
    try:
        # キーボード入力監視スレッドを開始
        exit_thread = Thread(target=monitor_exit, daemon=True)
        exit_thread.start()

        # イベント監視を開始
        event_thread = Thread(target=start_event_listener, daemon=True)
        event_thread.start()

        while not stop_flag.is_set():
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
        monitor_thread.join()
        console.info("プログラムを正常に終了しました。")
        exit(0)