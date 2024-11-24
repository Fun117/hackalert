from datetime import datetime
from src.colors import ColorManager
from src.setting import config

class CustomPrint:
    def __init__(self):
        self.config = config()
        color_config = self.config.get("colors", {})
        self.color_manager = ColorManager(color_config)  # ColorManagerのインスタンス作成
        self.console_config = self.config.get("console", {})

    def _apply_color(self, value, level):
        """
        `set_color` の設定に応じて色を適用する。
        """
        if value == "@auto":
            # ログレベルに対応する色を適用
            return self.color_manager.get_color(level, self.color_manager.get_color("reset", ""))
        elif value == "@none":
            # 色を適用しない（デフォルト色）
            return ""
        elif value.startswith("<") and value.endswith(">"):
            # 指定された色キーを適用
            color_key = value.strip("<>")
            return self.color_manager.get_color(color_key, "")
        else:
            # 不明な指定の場合、リセット色を使用
            return self.color_manager.get_color("reset", "")

    def _log(self, level, message):
        """ログを出力"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reset = self.color_manager.get_color("reset", "")

        # 各レベルの設定を取得
        level_config = self.console_config.get(level, {})
        color_config = level_config.get("color", {})
        log_format = level_config.get("format", "<level> <timestamp> <message>")

        # 色を適用
        level_color = self._apply_color(color_config.get("level", "@auto"), level)
        timestamp_color = self._apply_color(color_config.get("timestamp", "@none"), level)
        message_color = self._apply_color(color_config.get("message", "@none"), level)

        # フォーマットを取得して置き換え
        log_format = log_format.replace('<level>', f"{level_color}[{level.upper()}]{reset}")
        log_format = log_format.replace('<timestamp>', f"{timestamp_color}{timestamp}{reset}")
        log_format = log_format.replace('<message>', f"{message_color}{message}{reset}")

        # コンソールに出力
        print(log_format)

    def log(self, message):
        self._log("log", message)

    def info(self, message):
        self._log("info", message)

    def warning(self, message):
        self._log("warning", message)

    def error(self, message):
        self._log("error", message)

    def debug(self, message):
        self._log("debug", message)
