# 環境変数関連 ----------------------------------------------
import os
from dotenv import load_dotenv
import yaml

# 既存の環境変数をリセット
os.environ.clear()
# dotenv を再読み込み
load_dotenv()

# 環境変数を取得する関数
def env(key: str, default: str = None) -> str:
    return os.getenv(key, default)

# 設定ファイルを読み込む関数
def load_config(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

# 設定を取得
get_config = load_config(env('CONFIG_YML_FILE'))

def config():
    global get_config
    return get_config