import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw/DataScienceBasics_QandA - Sheet1.csv")

print("Gefundene Spalten:", df.columns.tolist())

df = df.rename(
    columns={
        "Question": "question",
        "Answer": "answer",
    }
)

df = df[["question", "answer"]]

Path("data/processed").mkdir(parents=True, exist_ok=True)
df.to_csv("data/processed/questions.csv", index=False)

print("Bereinigte CSV gespeichert.")
