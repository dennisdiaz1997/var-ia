import pandas as pd
import re

df = pd.read_csv("data/raw/champions_matches_raw.csv")

print("Columnas:", df.columns.tolist())

# renombrar columnas
df = df.rename(columns={
    "Date": "date",
    "Team 1": "home_team",
    "Team 2": "away_team"
})

# convertir fecha
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# función para extraer goles
def extract_goals(score):
    if isinstance(score, str) and re.match(r'^\d+-\d+$', score):
        home, away = score.split("-")
        return int(home), int(away)
    return None, None

df[["home_goals","away_goals"]] = df["FT"].apply(
    lambda x: pd.Series(extract_goals(x))
)

# eliminar filas sin goles válidos
df = df.dropna(subset=["home_goals","away_goals"])

# convertir a entero
df["home_goals"] = df["home_goals"].astype(int)
df["away_goals"] = df["away_goals"].astype(int)

# ordenar por fecha
df = df.sort_values("date")

# eliminar duplicados
df = df.drop_duplicates()

# guardar dataset limpio
df.to_csv("data/processed/champions_matches_clean.csv", index=False)

print("\nDataset limpio generado")
print("Filas finales:", len(df))