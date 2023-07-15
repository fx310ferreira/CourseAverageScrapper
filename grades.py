import pickle
import pandas as pd
from unidecode import unidecode


def join_grades():
    with open("grades.pkl", "rb") as f:
        grades = pickle.load(f)

    with open("grades1.pkl", "rb") as f:
        grades1 = pickle.load(f)

    for i in grades.keys():
        if(i in grades1.keys()):
            for j in grades[i].keys():
                if(j == "name"):
                    continue
                else:    
                    grades1[i][j] = grades[i][j]
        else:
            grades1[i] = grades[i]
    #remove students that are not in all courses
    array = []
    for i in grades1.keys():
        if len(grades1[i].keys()) != len(grades1["2021217116"].keys()):
            array.append(i)
    for i in array:
        del grades1[i]

    with open("allGrades.pkl", "wb") as f:
        pickle.dump(grades1, f)
    return grades1

# def dicToDF(dic):

grades = join_grades()
df = pd.DataFrame.from_dict(grades, orient='index')
column_avg = df.drop("name", axis=1).mean(axis=1)
for i in df.columns:
    name = ""
    for j in unidecode(i):
        if "A" <= j <= "Z":
            name += j
    df.rename(columns={i: name}, inplace=True)

df["avg"] = column_avg
df.sort_values(by="avg", ascending=False, inplace=True)
print(df)
df.to_csv("grades.csv")


