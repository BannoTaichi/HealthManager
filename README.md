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

## 各種パラメータ計算方法

### 食事の栄養素

- newFoodData_fromGovernment.csv(dataset)
- ユーザーの入力(input)

1. input.name と一致する dataset.name の行を抽出
2. dataset.dish_amount[g]と input.amount[g]の比(input.amount/dataset.dish_amount)を ratio として格納
   - 入力が無い場合は ratio = 1
3. dataset の各列のデータを取り出し、そこに ratio を乗算
4. 小数点第一位まで丸め込んだ値を摂取栄養素として記録

### 筋トレの消費カロリー

- TrainingData_60kg.csv(dataset)
- ユーザーの入力(input)
- ユーザーの設定(user)

1. input.name と一致する dataset.name の行を抽出
2. dataset.sets[count]と input.sets[count]の比(input.sets/dataset.sets)を sets_ratio として格納
   - 入力が無い場合は sets_ratio = 1
3. dataset.reps[count]と input.reps[count]の比(input.reps/dataset.reps)を reps_ratio として格納
   - 入力が無い場合は reps_ratio = 1
4. dataset.setTime[count]と input.setTime[count]の比(input.setTime/dataset.setTime)を setTime_ratio として格納
   - 入力が無い場合は setTime_ratio = 1
5. user.weight と 60 kg の比(user.weight/60)を weight_ratio として格納
   - 入力が無い場合は weight_ratio = 1
6. sets_ratio × reps_ratio × setTime_ratio × weight_ratio × dataset.energy[kcal]を消費カロリーとして記録
