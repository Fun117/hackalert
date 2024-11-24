from src.setting import config
from collections import defaultdict
from time import time
from src.console import CustomPrint
console = CustomPrint()

from src.log import Logger
logger = Logger()

class HackAlert:
    def __init__(self):
        self.config = config()
        # 更新回数の記録
        self.on_set_update_counts = defaultdict(int)  # 各変数の更新回数を保持
        self.on_set_last_reset_time = time()  # 更新回数をリセットした最後の時刻
        self.on_set_reset_interval = int(config()['alert']['on_set']['reset_interval']) # リセット間隔
        self.on_set_update_threshold = int(config()['alert']['on_set']['update_threshold'])
        self.on_set_output_log = config()['alert']['on_set']['output_log']

        self.on_del_update_counts = defaultdict(int)  # 各変数の更新回数を保持
        self.on_del_last_reset_time = time()  # 更新回数をリセットした最後の時刻
        self.on_del_reset_interval = int(config()['alert']['on_set']['reset_interval'])
        self.on_del_update_threshold = int(config()['alert']['on_del']['update_threshold'])
        self.on_del_output_log = config()['alert']['on_del']['output_log']

        self.on_create_update_counts = defaultdict(int)  # 各変数の更新回数を保持
        self.on_create_last_reset_time = time()  # 更新回数をリセットした最後の時刻
        self.on_create_reset_interval = int(config()['alert']['on_set']['reset_interval'])
        self.on_create_update_threshold = int(config()['alert']['on_create']['update_threshold'])
        self.on_create_output_log = config()['alert']['on_create']['output_log']

    def alert_on_set(self, activity: any):
        self._alert(activity, "on_set")

    def alert_on_del(self, activity: any):
        self._alert(activity, "on_del")

    def alert_on_create(self, activity: any):
        self._alert(activity, "on_create")

    def _alert(self, activity, event_type):
        # 現在の時刻を取得
        current_time = time()

        # イベントに関連する設定を取得
        if event_type == "on_set":
            counts_dict = self.on_set_update_counts
            last_reset_time = self.on_set_last_reset_time
            reset_interval = self.on_set_reset_interval
            update_threshold = self.on_set_update_threshold
            output_log_flag = self.on_set_output_log
        elif event_type == "on_del":
            counts_dict = self.on_del_update_counts
            last_reset_time = self.on_del_last_reset_time
            reset_interval = self.on_del_reset_interval
            update_threshold = self.on_del_update_threshold
            output_log_flag = self.on_del_output_log
        elif event_type == "on_create":
            counts_dict = self.on_create_update_counts
            last_reset_time = self.on_create_last_reset_time
            reset_interval = self.on_create_reset_interval
            update_threshold = self.on_create_update_threshold
            output_log_flag = self.on_create_output_log

        # タイムウィンドウを超えた場合、更新回数をリセット
        if current_time - last_reset_time > reset_interval:
            counts_dict.clear()
            if event_type == "on_set":
                self.on_set_last_reset_time = current_time
            elif event_type == "on_del":
                self.on_del_last_reset_time = current_time
            elif event_type == "on_create":
                self.on_create_last_reset_time = current_time

        # イベントの更新回数をカウント
        event_key = activity.var if event_type != "on_create" else activity.user
        counts_dict[event_key] += 1

        # フォーマット文字列を設定
        format_str = str(self.config.get("alert", {}).get(event_type, {}).get("format", "Event <event_type> by <key> exceeded the threshold (<threshold> times). Current: <count> times in <interval> seconds"))
        format_str = format_str.replace('<event_type>', event_type)
        format_str = format_str.replace('<key>', str(activity.var if event_type != "on_create" else activity.user))
        format_str = format_str.replace('<threshold>', str(update_threshold))
        format_str = format_str.replace('<count>', str(counts_dict[event_key]))
        format_str = format_str.replace('<interval>', str(reset_interval))

        # 閾値を超えた場合に警告を出力
        if counts_dict[event_key] >= update_threshold:  # >= に修正
            console.warning(format_str)
            if bool(output_log_flag) == True:
                logger.log_message(format_str)