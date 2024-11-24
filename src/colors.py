from colorama import init

init()  # ANSIコードの有効化

class ColorManager:
    def __init__(self, color_config):
        """
        コンストラクタで設定を受け取り、ANSIエスケープシーケンスを生成。
        """
        self.colors = self._generate_colors(color_config)

    def _generate_colors(self, color_config):
        """
        設定からANSIエスケープシーケンスを生成。
        """
        ansi_prefix = "\033["  # ANSIエスケープシーケンスのプレフィックス
        return {key: f"{ansi_prefix}{value}" for key, value in color_config.items()}

    def get_color(self, key, default=""):
        """
        指定されたキーの色を取得。存在しない場合はデフォルト値を返す。
        """
        return self.colors.get(key, default)

    def apply_color(self, value, color_key, default=""):
        """
        指定したキーの色を文字列に適用。
        """
        color = self.get_color(color_key, default)
        reset = self.get_color("reset", "")
        return f"{color}{value}{reset}"