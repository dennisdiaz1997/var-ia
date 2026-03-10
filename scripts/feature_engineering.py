import pandas as pd

# cargar dataset limpio
df = pd.read_csv("data/processed/champions_matches_clean.csv")

# convertir fecha
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ordenar cronológicamente
df = df.sort_values("date").reset_index(drop=True)

def get_result(row):
    if row["home_goals"] > row["away_goals"]:
        return "H"
    elif row["home_goals"] < row["away_goals"]:
        return "A"
    else:
        return "D"

def get_points(team, row):
    if row["home_team"] == team:
        if row["home_goals"] > row["away_goals"]:
            return 3
        elif row["home_goals"] == row["away_goals"]:
            return 1
        else:
            return 0
    elif row["away_team"] == team:
        if row["away_goals"] > row["home_goals"]:
            return 3
        elif row["away_goals"] == row["home_goals"]:
            return 1
        else:
            return 0
    return 0

def last_matches(history, team, n=5):
    return history[
        (history["home_team"] == team) | (history["away_team"] == team)
    ].tail(n)

def calculate_form(history, team, n=5):
    matches = last_matches(history, team, n)
    return sum(get_points(team, row) for _, row in matches.iterrows())

def calculate_avg_goals(history, team, n=5):
    matches = last_matches(history, team, n)
    if matches.empty:
        return 0.0

    goals = []
    for _, row in matches.iterrows():
        if row["home_team"] == team:
            goals.append(row["home_goals"])
        else:
            goals.append(row["away_goals"])
    return round(sum(goals) / len(goals), 2)

def calculate_avg_conceded(history, team, n=5):
    matches = last_matches(history, team, n)
    if matches.empty:
        return 0.0

    conceded = []
    for _, row in matches.iterrows():
        if row["home_team"] == team:
            conceded.append(row["away_goals"])
        else:
            conceded.append(row["home_goals"])
    return round(sum(conceded) / len(conceded), 2)

# features básicas
df["result"] = df.apply(get_result, axis=1)
df["goal_difference"] = df["home_goals"] - df["away_goals"]
df["total_goals"] = df["home_goals"] + df["away_goals"]
df["home_advantage"] = 1

# features avanzadas
home_form_5 = []
away_form_5 = []
home_avg_goals_5 = []
away_avg_goals_5 = []
home_avg_conceded_5 = []
away_avg_conceded_5 = []

for idx, row in df.iterrows():
    history = df.iloc[:idx]

    home_team = row["home_team"]
    away_team = row["away_team"]

    home_form_5.append(calculate_form(history, home_team, 5))
    away_form_5.append(calculate_form(history, away_team, 5))

    home_avg_goals_5.append(calculate_avg_goals(history, home_team, 5))
    away_avg_goals_5.append(calculate_avg_goals(history, away_team, 5))

    home_avg_conceded_5.append(calculate_avg_conceded(history, home_team, 5))
    away_avg_conceded_5.append(calculate_avg_conceded(history, away_team, 5))

df["home_form_5"] = home_form_5
df["away_form_5"] = away_form_5
df["home_avg_goals_5"] = home_avg_goals_5
df["away_avg_goals_5"] = away_avg_goals_5
df["home_avg_conceded_5"] = home_avg_conceded_5
df["away_avg_conceded_5"] = away_avg_conceded_5

# opcional: dejar solo columnas útiles
final_columns = [
    "date",
    "season",
    "Stage",
    "Group",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
    "result",
    "goal_difference",
    "total_goals",
    "home_advantage",
    "home_form_5",
    "away_form_5",
    "home_avg_goals_5",
    "away_avg_goals_5",
    "home_avg_conceded_5",
    "away_avg_conceded_5"
]

# conservar solo las columnas que existan
final_columns = [col for col in final_columns if col in df.columns]
df = df[final_columns]

# guardar dataset final
df.to_csv("data/processed/champions_matches_clean.csv", index=False)

print("Feature engineering completado")
print("Columnas finales:", df.columns.tolist())
print("Total de filas:", len(df))