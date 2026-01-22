from pathlib import Path

import pandas as pd

df = pd.read_csv("data/raw/DataScienceBasics_QandA - Sheet1.csv")

print("Gefundene Spalten:", df.columns.tolist())

df = df.rename(
    columns={
        "Question": "question",
        "Answer": "answer",
    }
)

df = df[["question", "answer"]]
df["max_points"] = 5

Path("data/processed").mkdir(parents=True, exist_ok=True)
df.to_csv("data/processed/questions.csv", index=False)

print("Bereinigte CSV gespeichert.")
