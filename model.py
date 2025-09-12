import pandas as pd


def calc_nutrient(meal, amount):
    food_df = pd.read_csv("csv/newFoodData_fromGovernment.csv", index_col=0)
    if meal in food_df.index:
        nutrient_info = food_df.loc[meal]

        if not amount:
            amount = int(nutrient_info["dish_amount[g]"])
            ratio = 1

        if int(amount) != int(nutrient_info["dish_amount[g]"]):
            ratio = int(amount) / int(nutrient_info["dish_amount[g]"])

        energy = round(float(nutrient_info["energy[kcal]"]) * ratio, 1)
        protein = round(float(nutrient_info["protein[g]"]) * ratio, 1)
        carbs = round(float(nutrient_info["carbs[g]"]) * ratio, 1)
        fat = round(float(nutrient_info["fat[g]"]) * ratio, 1)
        vitamins = round(float(nutrient_info["vitamins[mg]"]) * ratio, 1)
        minerals = round(float(nutrient_info["minerals[mg]"]) * ratio, 1)

        print(f"Meal: {meal}, Amount: {amount}g")
        print(
            f"Protein: {protein}g, Carbs: {carbs}g, Fat: {fat}g, Vitamins: {vitamins}mg, Minerals: {minerals}mg"
        )
        return amount, energy, protein, carbs, fat, vitamins, minerals
    else:
        return 0, 0, 0, 0, 0, 0, 0


def calc_total_nutrients(meal_logs):
    total_nutrients = {
        "energy": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "vitamins": 0,
        "minerals": 0,
    }

    for log in meal_logs:
        total_nutrients["energy"] += log.energy
        total_nutrients["protein"] += log.protein
        total_nutrients["carbs"] += log.carbs
        total_nutrients["fat"] += log.fat
        total_nutrients["vitamins"] += log.vitamins
        total_nutrients["minerals"] += log.minerals

    print(
        f"""Total energy: {round(total_nutrients['energy'] ,1)} kcal
            Total protein: {round(total_nutrients['protein'] ,1)} g
            Total carbs: {round(total_nutrients['carbs'] ,1)} g
            Total fat: {round(total_nutrients['fat'] ,1)} g
            Total vitamins: {round(total_nutrients['vitamins'] ,1)} mg
            Total minerals: {round(total_nutrients['minerals'] ,1)} mg"""
    )
    return total_nutrients


def calc_burned_calories(sets, reps, setTime, stretch):
    df = pd.read_csv("csv/TrainingData_60kg.csv", index_col=0)
    if stretch in df.index:
        try:
            sets_ratio = int(sets) / int(df.loc[stretch, "sets[count]"])
        except:
            sets_ratio = 1
        try:
            reps_ratio = int(reps) / int(df.loc[stretch, "reps[count]"])
        except:
            reps_ratio = 1
        try:
            setTime_ratio = int(setTime) / int(df.loc[stretch, "setTime[sec]"])
        except:
            setTime_ratio = 1

        energy = round(
            float(df.loc[stretch, "energy[kcal]"])
            * sets_ratio
            * reps_ratio
            * setTime_ratio,
            1,
        )
    else:
        energy = 0
    return energy


if __name__ == "__main__":
    meal = "ビーフカレー"
    amount = 200
    amount, energy, protein, carbs, fat, vitamins, minerals = calc_nutrient(
        meal, amount
    )
