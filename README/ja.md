# Scratch ハックアラート

Scratch のクラウド変数の値を監視し、悪意のある変更やクラウドハックを検出します。

#### クラウドハックとは

クラウド変数を外部ツールを使用して、変数を悪意のある値に変更したり、変数を高速で変更するなどのことを指します。

## 環境変数の設定

環境変数では Scratch アカウントの情報などを設定します。

```env
USERNAME=*****
PASSWORD=*****
CONFIG_YML_FILE=*******
```

- `USERNAME`: アカウントのユーザー名
- `PASSWORD`: アカウントのパスワード
- `CONFIG_YML_FILE`: 設定ファイルのパスを入力してください。ファイル端子は `yml` である必要があります。

## 設定ファイル

```yml
lang: ja
project_id: 843162693

colors:
  reset: "0m" # default
  log: "36m" # cyan
  info: "32m" # green
  warning: "33m" # yellow
  error: "31m" # red
  debug: "34m" # blue
  success: "92m" # bright green
  critical: "95m" # magenta
  note: "35m" # purple

logs:
  timestamp: true
  output:
    directory: ./logs
    format: "<level> <timestamp> <message>"
  on_set:
    format: "変数 <var> は、<timestamp> に値 <value> に設定されました"
    colors:
      var: "critical"
      value: "success"
      timestamp: "log"
  on_del:
    format: "<user> が変数 <var> を削除しました"
    colors:
      var: "warning"
  on_create:
    format: "<user> が変数 <var> を作成しました"
    colors:
      var: "success"
  on_ready:
    message: "イベントリスナーの準備ができました！"

console:
  log:
    color:
      level: "<log>"
      message: "@none"
      timestamp: "@none"
    format: "<level> <timestamp> <message>"
  info:
    color:
      level: "<info>"
      message: "@none"
      timestamp: "@none"
    format: "<level> <timestamp> <message>"
  warning:
    color:
      level: "<warning>"
      message: "<warning>"
      timestamp: "<warning>"
    format: "<level> <timestamp> <message>"
  error:
    color:
      level: "<error>"
      message: "<error>"
      timestamp: "<error>"
    format: "<level> <timestamp> <message>"
  debug:
    color:
      level: "<debug>"
      message: "@none"
      timestamp: "@none"
    format: "<level> <timestamp> <message>"

alert:
  on_set:
    reset_interval: 1
    update_threshold: 2
    format: "変数 <var> の更新回数が閾値 (<update_threshold> 回) を超えました (現在: <updates_count> 回 / <reset_interval> 秒)"
    output_log: false
  on_del:
    reset_interval: 1
    update_threshold: 1
    format: "イベント <event_type> による <key> が閾値 (<threshold> 回) を超えました (現在: <count> 回 / <interval> 秒)"
    output_log: false
  on_create:
    reset_interval: 1
    update_threshold: 1
    format: "イベント <event_type> による <key> が閾値 (<threshold> 回) を超えました (現在: <count> 回 / <interval> 秒)"
    output_log: false
```

- `config.yml`

  - `lang`: 使用する言語を選択してください。
  - `project_id`: 監視したい Scratch プロジェクトの ID を入力してください。

  - `logs`

    - `output`

      - `directory`: ログファイルを出力するディレクトリを指定します。
      - `format`: 出力するメッセージのフォーマットを設定します。

    - `on_set`

      - `format`: ログメッセージのフォーマットを設定します。以下の項目を使用できます。項目名は `< >` で囲む必要があります。
        - `var`: 変数名
        - `value`: 変数の値
        - `timestamp`: タイムスタンプ
        - `username`: ユーザー名
        - `decode`: 復号した値を出力（ScratchAttach の暗号化方法を使用）

    - `on_del`

      - `format`: ログメッセージのフォーマットを設定します。以下の項目を使用できます。項目名は `< >` で囲む必要があります。
        - `var`: 変数名
        - `user`: ユーザー

    - `on_create`

      - `format`: ログメッセージのフォーマットを設定します。以下の項目を使用できます。項目名は `< >` で囲む必要があります。
        - `var`: 変数名
        - `user`: ユーザー

    - `on_ready`
      - `message`: 監視の準備が完了した際に表示されるメッセージ。

  - `console`

    - `set_color`:

      - `level`: ログレベルに対応する色を指定します。`@auto` は自動設定です。
      - `timestamp`: タイムスタンプに対応する色を指定します。
      - `message`: メッセージに対応する色を指定します。`@none` は色なしです。

    - `format`: コンソールに表示するログのフォーマットを設定します。

  - `alert`

    - `on_set`:

      - `reset_interval`: 更新回数がリセットされる秒数を指定します。
      - `update_threshold`: 更新回数の閾値を設定します。これを超えるとアラートが発生します。
      - `format`: アラートメッセージのフォーマットを設定します。項目名は `< >` で囲む必要があります。
      - `output_log`: アラート時にログを出力するかどうかを指定します。`false` の場合はログ出力なしです。

## カスタムカラーの設定

以下にカラー設定を追加することで、カスタムカラーを追加できます。各項目は `<色名>` を `colors` セクションに追加し、設定を反映してください。

| カラー名   | 説明                   | 設定例 |
| ---------- | ---------------------- | ------ |
| `reset`    | デフォルトの色         | "0m"   |
| `log`      | ログ用カラー           | "36m"  |
| `info`     | 情報用カラー           | "32m"  |
| `warning`  | 警告用カラー           | "33m"  |
| `error`    | エラー用カラー         | "31m"  |
| `debug`    | デバッグ用カラー       | "34m"  |
| `success`  | 成功メッセージ用カラー | "92m"  |
| `critical` | 重要メッセージ用カラー | "95m"  |
| `note`     | 注意メッセージ用カラー | "35m"  |
