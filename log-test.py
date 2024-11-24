from src.setting import env, config
from src.console import CustomPrint
console = CustomPrint()
from src.colors import ColorManager  # ColorManager のインポート
color_manager = ColorManager(config().get("colors", {}))
color_reset = color_manager.get_color('reset', '')
def get_color(key: str):
    return color_manager.get_color(key,'')

from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"\033[106m Log \033[0m " + f"{timestamp}")
print(f"\033[43m Warn \033[0m")
print(f"\033[101m Error \033[0m")

console.log("Hello")
console.warning("Hello")
console.error("Hello")
console.debug("Hello")
console.info("Hello")

import textwrap

print(textwrap.dedent("""
=======================================

    \033[1;101mScratch Cloud Event Monitor\033[0m
    ___________________________
    
    起動構成:
    - ユーザー名: ********
    - プロジェクトID: ********

=======================================
"""))

print("Hello")