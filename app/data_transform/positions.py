import polars as pl

year = "2025"

calendar_df = pl.read_json(f"data/{year}/{year}_calendar.json").select(
    pl.col("round").alias("round_number"),
    pl.col("displayed_text").alias("round_name"),
)

dfs = []
for round_number in range(1, len(calendar_df) + 1):
    round_path = f"data/{year}/round_{round_number}/race.json"

    df = pl.read_json(round_path).select(
        pl.lit(round_number).alias("round_number"),
        "position",
        "rider",
        "points",
    )

    dfs.append(df)

all_races = pl.concat(dfs, how="vertical")

all_races = all_races.join(calendar_df, on="round_number", how="inner")
