import pandas as pd
import pytz
from datetime import datetime, timedelta
from database import db, User, MealLog, StretchLog, Post


# csvフォルダ内の食品データを用いて、食品名と量から栄養素を計算する関数
def calc_nutrient_from_table(meal, amount):
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

        print(f"<<<Meal: {meal}, Amount: {amount}g from calc_nutrient_from_table()>>>")
        print(
            f"Protein: {protein}g, Carbs: {carbs}g, Fat: {fat}g, Vitamins: {vitamins}mg, Minerals: {minerals}mg\n"
        )
        return amount, energy, protein, carbs, fat, vitamins, minerals
    else:
        return 0, 0, 0, 0, 0, 0, 0


# 集計した範囲の食事ログを用いて、総摂取栄養素を計算する関数
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

    print("<<<Total nutrients from calc_total_nutrients()>>>")
    print(
        f"energy: {round(total_nutrients['energy'] ,1)}kcal, protein: {round(total_nutrients['protein'] ,1)}g, carbs: {round(total_nutrients['carbs'] ,1)}g, fat: {round(total_nutrients['fat'] ,1)}g, vitamins: {round(total_nutrients['vitamins'] ,1)}mg, minerals: {round(total_nutrients['minerals'] ,1)}mg\n"
    )
    return total_nutrients


# csvフォルダ内のトレーニングデータを用いて、ストレッチ内容・回数・時間・体重から消費カロリーを計算する関数
def calc_burned_calories(stretch, sets, reps, setTime, weight=60):
    df = pd.read_csv("csv/TrainingData_60kg.csv", index_col=0)
    if stretch in df.index:
        weight_ratio = weight / 60
        try:
            sets_ratio = round(int(sets) / int(df.loc[stretch, "sets[count]"]), 1)
        except:
            sets_ratio = 1
        try:
            reps_ratio = round(int(reps) / int(df.loc[stretch, "reps[count]"]), 1)
        except:
            reps_ratio = 1
        try:
            setTime_ratio = round(
                int(setTime) / int(df.loc[stretch, "setTime[sec]"]), 1
            )
        except:
            setTime_ratio = 1

        if type(reps_ratio) == float and type(setTime_ratio) == float:
            energy = round(
                float(df.loc[stretch, "energy[kcal]"])
                * sets_ratio
                * min(reps_ratio, setTime_ratio)
                * weight_ratio,
                1,
            )
        else:
            energy = round(
                float(df.loc[stretch, "energy[kcal]"])
                * sets_ratio
                * reps_ratio
                * setTime_ratio
                * weight_ratio,
                1,
            )

        print(
            f"<<<Burned calories for {stretch}: {energy} kcal from calc_burned_calories()>>>"
        )
        print(
            f"sets ratio: {sets_ratio}, reps ratio: {reps_ratio}, setTime ratio: {setTime_ratio}, weight ratio: {weight_ratio}, base energy: {df.loc[stretch, 'energy[kcal]']}kcal\n"
        )
    else:
        energy = 0
    return energy


# 指定したデータベースの指定範囲のログを返す関数
def get_recent_logs(Log, hours, user_id):
    time_now = datetime.now(pytz.timezone("Asia/Tokyo"))
    time_ago = time_now - timedelta(hours=hours)
    recent_logs = (
        db.session.query(Log)
        .filter(
            Log.user_id == user_id,
            Log.date >= time_ago,
            Log.date <= time_now,
        )
        .all()
    )
    print(f"<<<{hours}-hour {Log.__name__} from get_recent_logs()>>>")
    for log in recent_logs:
        if Log == MealLog:
            print(
                f"Date: {log.date.strftime('%Y-%m-%d %H:%M')}, {Log.__name__[:-3]}: {getattr(log, Log.__name__.lower()[:-3])}, Amount: {getattr(log, 'amount', 'N/A')}g, Calories: {getattr(log, 'energy', 'N/A')}kcal"
            )
        elif Log == StretchLog:
            print(
                f"Date: {log.date.strftime('%Y-%m-%d %H:%M')}, {Log.__name__[:-3]}: {getattr(log, Log.__name__.lower()[:-3])}, Sets: {getattr(log, 'sets', 'N/A')}, Reps: {getattr(log, 'reps', 'N/A')}, Time: {getattr(log, 'setTime', 'N/A')}s, Calories: {getattr(log, 'energy', 'N/A')}kcal"
            )
    return recent_logs


if __name__ == "__main__":
    meal = "ビーフカレー"
    amount = 200
    amount, energy, protein, carbs, fat, vitamins, minerals = calc_nutrient_from_table(
        meal, amount
    )

    stretch = "腕立て伏せ"
    sets = 3
    reps = 15
    setTime = 30
    weight = 90
    energy = calc_burned_calories(stretch, sets, reps, setTime, weight)
