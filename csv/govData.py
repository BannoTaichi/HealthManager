import pandas as pd

dish_weights = [
    250,  # ビーフカレー
    120,  # ぎょうざ
    200,  # えびグラタン
    180,  # コーンクリームスープ
    100,  # クリームコロッケ
    90,  # ポテトコロッケ
    100,  # いかフライ
    80,  # えびフライ
    100,  # 白身フライ
    250,  # ビーフシチュー
    100,  # しゅうまい
    250,  # えびピラフ
    120,  # ミートボール
    120,  # メンチカツ
    90,  # ポテトコロッケ（重複）
    100,  # いかフライ（重複）
    80,  # えびフライ（重複）
    100,  # 白身フライ（重複）
    120,  # メンチカツ（重複）
    80,  # 松前漬け
    100,  # 青菜の白和え
    80,  # いんげんのごま和え
    80,  # わかめとねぎの酢みそ和え
    100,  # 紅白なます
    200,  # とん汁
    120,  # 卯の花いり
    200,  # 親子丼の具
    200,  # 牛飯の具
    120,  # 切り干し大根の煮物
    100,  # きんぴらごぼう
    100,  # ぜんまいのいため煮
    200,  # 筑前煮
    220,  # 肉じゃが
    100,  # ひじきのいため煮
    150,  # アジの南蛮漬け
    100,  # もやしのナムル
    250,  # チキンカレー
    250,  # ポークカレー
    180,  # かぼちゃのクリームスープ
    100,  # カニクリームコロッケ
    100,  # コーンクリームコロッケ
    250,  # チキンシチュー
    180,  # 中華ちまき
    200,  # 酢豚
    220,  # 八宝菜
    220,  # 麻婆豆腐
    150,  # 合いびきハンバーグ
    150,  # チキンハンバーグ
    150,  # 豆腐ハンバーグ
    300,  # お好み焼き
    150,  # とりから揚げ
    100,  # かきフライ
    120,  # 春巻き
    250,  # チャーハン
]

df = pd.read_csv("FoodData_fromGovernment.csv")
df = df.drop("id", axis=1, errors="ignore")
df["dish_amount[g]"] = dish_weights
df = df.reindex(
    columns=[
        "name",
        "base_amount[g]",
        "dish_amount[g]",
        "energy[kcal]",
        "protein[g]",
        "carbs[g]",
        "fat[g]",
        "vitamins[mg]",
        "minerals[mg]",
    ]
)
df["energy[kcal]"] = round(
    df["energy[kcal]"] * df["dish_amount[g]"] / df["base_amount[g]"], 1
)
df["protein[g]"] = round(
    df["protein[g]"] * df["dish_amount[g]"] / df["base_amount[g]"], 1
)
df["carbs[g]"] = round(df["carbs[g]"] * df["dish_amount[g]"] / df["base_amount[g]"], 1)
df["fat[g]"] = round(df["fat[g]"] * df["dish_amount[g]"] / df["base_amount[g]"], 1)
df["vitamins[mg]"] = round(
    df["vitamins[mg]"] * df["dish_amount[g]"] / df["base_amount[g]"], 1
)
df["minerals[mg]"] = round(
    df["minerals[mg]"] * df["dish_amount[g]"] / df["base_amount[g]"], 1
)
df = df.drop("base_amount[g]", axis=1, errors="ignore")

index = df["name"].to_list()
df.index = index
df = df.drop("name", axis=1, errors="ignore")
df.to_csv("newFoodData_fromGovernment.csv")

if __name__ == "__main__":
    print(df)
