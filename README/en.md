# Scratch Hack Alert

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

- `USERNAME`: Account username
- `PASSWORD`: Account password
- `CONFIG_YML_FILE`: 設定ファイルのパスを入力してください。ファイル端子は `yml` である必要があります。

## 設定ファイル

```yml
lang: en
project_id: 843162693
logs:
  output_directory: ./logs
  on_set:
    format: "Variable <var> was set to the value <value> at <timestamp>"
  on_del:
    format: "<user> deleted variable <var>"
  on_create:
    format: "<user> created variable <var>"
  on_ready:
    message: "Event listener ready!"
```

- `lang` 対応している言語から選択してください。

- `project_id`: 監視したい Scratch プロジェクトの ID を入力してください。

- `logs`

  - `output_directory`: ログファイルの出力ディレクトリーを指定します。

  - `on_set`

    - `format`: ログメッセージのフォーマットを設定します。

      以下の項目を使用することが出来ます。項目名を `<>` で囲むこ必要があります。

      - `var`: 変数名
      - `value`: 変数の値
      - `timestamp`: タイムスタンプ
      - `username`: ユーザー名
      - `decode`: 値を復号をした値を出力（ScratchAttach が提供している暗号化方法を使用している）

  - `on_del`

    - `format`: ログメッセージのフォーマットを設定します。

      以下の項目を使用することが出来ます。項目名を `<>` で囲むこ必要があります。

      - `var`: 変数名
      - `user`: ユーザー

  - `on_create`

    - `format`: ログメッセージのフォーマットを設定します。

      以下の項目を使用することが出来ます。項目名を `<>` で囲むこ必要があります。

      - `var`: 変数名
      - `user`: ユーザー

  - `on_ready`

    - `message`: 変数の監視準備ができた時のメッセージ
