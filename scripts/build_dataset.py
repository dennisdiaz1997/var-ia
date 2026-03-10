import pandas as pd
import os

base_path = "champions-league"

all_matches = []

for season in os.listdir(base_path):

    season_path = os.path.join(base_path, season)

    if os.path.isdir(season_path):

        file_path = os.path.join(season_path, "champs.csv")

        if os.path.exists(file_path):

            df = pd.read_csv(file_path)

            df["season"] = season

            all_matches.append(df)

            print("Cargando:", file_path)

dataset = pd.concat(all_matches, ignore_index=True)

dataset.to_csv("data/raw/champions_matches_raw.csv", index=False)

print("\nDataset combinado generado")
print("Total partidos:", len(dataset))