import pandas as pd

df = pd.read_csv("FoodData_fromKurumeOpenData.csv", index_col=0)
index = df["name"].tolist()
df.index = index
df = df.drop("name", axis=1, errors="ignore")
print(df)
df.to_csv("newFoodData_fromKurumeOpenData.csv")
