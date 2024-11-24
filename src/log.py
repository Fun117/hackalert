import os
from datetime import datetime
from src.setting import config
from src.colors import ColorManager  # ColorManager をインポート

class Logger:
    def __init__(self):
        self.log_file = None
        self.config = config()

        # カラー設定の読み込みと初期化
        color_config = self.config.get("colors", {})
        self.color_manager = ColorManager(color_config)

        self.default_format = self.config.get("logs", {}).get("output", {}).get("format", "<level> <timestamp> <message>")

    def setup_logging(self):
        """ログファイルの設定を初期化"""
        output_directory = self.config.get('logs', {}).get('output', {}).get('directory', './')
        os.makedirs(output_directory, exist_ok=True)  # ディレクトリを自動作成
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(output_directory, f"{timestamp}.log")

        # ログファイルの作成メッセージを色付きで表示
        info_color = self.color_manager.get_color('info', '')
        reset_color = self.color_manager.get_color('reset', '')
        print(f"ログファイル: {info_color}{self.log_file}{reset_color} を作成しました。")

        if self.log_file:
            with open(self.log_file, 'a') as f:  # 追記モードでファイルを開く
                f.write(f"Project ID: {self.config['project_id']} / Start: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n")

    def log_message(self, message: str, level: str = "log"):
        """ログメッセージを保存"""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_format = self.default_format
        log_format = log_format.replace('<level>', f"[{level.upper()}]")
        log_format = log_format.replace('<timestamp>', f"{timestamp}")
        log_format = log_format.replace('<message>', f"{message}")

        # ファイルにログを書き込む
        if self.log_file:
            with open(self.log_file, 'a') as f:  # 追記モードでファイルを開く
                f.write(f"{log_format}\n")