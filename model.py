import pandas as pd


def calc_nutrient(meal, amount):
    food_df = pd.read_csv("csv/newFoodData_fromGovernment.csv", index_col=0)
    if meal in food_df.index:
        nutrient_info = food_df.loc[meal]

        if not amount:
            amount = nutrient_info["dish_amount[g]"]
            ratio = 1

        if amount != nutrient_info["dish_amount[g]"].values[0]:
            ratio = int(amount) / float(nutrient_info["dish_amount[g]"].values[0])

        protein = round(float(nutrient_info["protein[g]"].values[0]) * ratio, 1)
        carbs = round(float(nutrient_info["carbs[g]"].values[0]) * ratio, 1)
        fat = round(float(nutrient_info["fat[g]"].values[0]) * ratio, 1)
        vitamins = round(float(nutrient_info["vitamins[mg]"].values[0]) * ratio, 1)
        minerals = round(float(nutrient_info["minerals[mg]"].values[0]) * ratio, 1)

        print(f"Meal: {meal}, Amount: {amount}g")
        print(
            f"Protein: {protein}g, Carbs: {carbs}g, Fat: {fat}g, Vitamins: {vitamins}mg, Minerals: {minerals}mg"
        )
        return protein, carbs, fat, vitamins, minerals
    else:
        return 0, 0, 0, 0, 0


if __name__ == "__main__":
    meal = "ビーフカレー"
    amount = 200
    protein, carbs, fat, vitamins, minerals = calc_nutrient(meal, amount)
