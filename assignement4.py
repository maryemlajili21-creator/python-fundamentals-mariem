import pandas as pd
from functools import partial

# -----------------------------
# Step 1: Example weather data
# -----------------------------
data = {
    "Time": ["2025-01-01 00:00", "2025-01-01 01:00", "2025-01-01 02:00", "2025-01-01 03:00"],
    "Weather": ["Clear", "Cloudy", "Rain", "Clear"],
    "Temperature (C)": ["15.0", "14.5", "13.2", "12.0"],  # string to demonstrate type conversion
    "Apparent Temperature (C)": ["15.0", "14.0", "13.0", "12.0"],
    "Humidity": [0.70, 0.72, 0.80, None],  # include a missing value
    "Wind Speed (km/h)": [10, 12, 8, 5]
}

weather_df = pd.DataFrame(data)
weather_df.to_csv("weather.csv", index=False)

# -----------------------------
# Step 2: Custom Series
# -----------------------------
humidity_series = pd.Series([0.70, 0.72, 0.80, 0.65], index=["CityA", "CityB", "CityC", "CityD"])
print(humidity_series)

# -----------------------------
# Step 3: Create DataFrame with all needed columns
# -----------------------------
df = pd.DataFrame(weather_df, columns=[
    "Time", "Weather", "Temperature (C)", "Apparent Temperature (C)", "Humidity"
])
print(df)

# -----------------------------
# Step 4: Inspect DataFrame
# -----------------------------
print(df.dtypes)
print(df.head())
print(df.tail())
print(df.describe())

# -----------------------------
# Step 5: Slicing
# -----------------------------
# By row position
print(df.iloc[0:2])

# By column name
print(df[["Time", "Temperature (C)"]])

# Boolean flags: Humidity > 0.7
flag = df["Humidity"] > 0.7
print(df[flag])

# Temperature range between 13 and 15
print(df[(pd.to_numeric(df["Temperature (C)"]) >= 13) &
         (pd.to_numeric(df["Temperature (C)"]) <= 15)])

# -----------------------------
# Step 6: Duplicates
# -----------------------------
df_dup = pd.concat([df, df.iloc[[0]]], ignore_index=True)
print("Number of duplicates:", df_dup.duplicated().sum())
print("Unique counts:", df_dup.nunique())
df_clean = df_dup.drop_duplicates()
print(df_clean)

# -----------------------------
# Step 7: Type conversion
# -----------------------------
df["Temperature (C)"] = pd.to_numeric(df["Temperature (C)"])
df["Apparent Temperature (C)"] = pd.to_numeric(df["Apparent Temperature (C)"])
df["Time"] = pd.to_datetime(df["Time"])
print(df.dtypes)

# -----------------------------
# Step 8: Fill missing data
# -----------------------------
df["Humidity"] = df["Humidity"].apply(lambda x: 0.5 if pd.isnull(x) else x)
print(df)

# -----------------------------
# Step 9: Pipeline using .pipe()
# -----------------------------
def safe_convert(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
    return df

df = df.pipe(safe_convert, "Temperature (C)")
print(df.dtypes)

def threshold_filter(df, col_name, threshold):
    return df[df[col_name] >= threshold]

df_filtered = df.pipe(partial(threshold_filter, col_name="Temperature (C)", threshold=13))
print(df_filtered)
