## 環境

- conda create -n imanyu python=3.12
- conda-requirements.txt
- requirements.txt

## 使い方

1. create_db.py でデータベース instance/blog.db を作成
2. app.py で Flask アプリ起動

## 構成・各ファイルの説明

### アプリに必要なフォルダ

- csv フォルダ
  - ダウンロードしたデータセットの csv ファイルを収録
  - csv ファイルを本アプリで使いやすいように前処理するための python ファイルを収録
- instance フォルダ
  - create_db.py を実行すると、本フォルダ配下に blog.db というデータベースファイルが保存される
- templates フォルダ
  - Flask アプリに必要な各ページを、それぞれ HTML ファイルとして収録

### アプリの実行に必要な python ファイル

- app.py
  - Flask アプリを起動する際に実行するファイル
  - ルーティングと HTML の連携や、各変数の操作を担う
- create_db.py
  - Flask アプリを起動する前に、データベースを作成するために実行するファイル

### 冗長なコードを防ぐために分離したファイル

- database.py
  - 本アプリに必要なデータベースクラスを設定したファイル
  - `app.py`が長くなり過ぎないように、データベースクラスのみの本ファイルを用意
- model.py
  - `app.py`内で実行する操作の関数を収録
  - `app.py`が長くなり過ぎないように、長文の操作の関数を用意

### 無くてもいいが、あると便利なファイル

- conda-requirements.txt
  - `conda install`でインストールする本アプリに必要なライブラリのバージョンを記録
- requirements.txt
  - `pip install`でインストールする本アプリに必要なライブラリのバージョンを記録
- .gitignore
  - Git, GitHub にコミット・プッシュする際にコミットの対象外としたいフォルダ・ファイルを指定
