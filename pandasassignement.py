# ===============================================================
# 🧠 Pandas Mastery Assignment — Weather Data Manipulation
# ===============================================================
# Sources:
# - https://pandas.pydata.org/docs/
# - https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
# - https://docs.python.org/3/library/functools.html

import pandas as pd
from functools import partial

# ---------------------------------------------------------------
# 1️⃣ Create an example data file (we’ll use your uploaded weather.csv)
# ---------------------------------------------------------------
df = pd.read_csv("weather.csv")
print("✅ Weather dataset loaded successfully!\n")
print(df.head(), "\n")

# ---------------------------------------------------------------
# 2️⃣ Define a Pandas Series with a custom index
# ---------------------------------------------------------------
city_avg_temp = pd.Series(
    [14.2, 19.5, 11.3, 25.1],
    index=["Paris", "Madrid", "Berlin", "Tunis"]
)
print("Custom Series (Average Temperature by City):\n", city_avg_temp, "\n")

# ---------------------------------------------------------------
# 3️⃣ Create a Pandas DataFrame with specified columns
# ---------------------------------------------------------------
weather_df = df[
    ["Time", "Weather", "Temperature (C)", "Humidity", "Wind Speed (km/h)"]
]
print("DataFrame with selected columns:\n", weather_df.head(), "\n")

# ---------------------------------------------------------------
# 4️⃣ Inspect the DataFrame using dtypes, head/tail, and describe
# ---------------------------------------------------------------
print("Data types:\n", weather_df.dtypes, "\n")
print("First 3 rows:\n", weather_df.head(3), "\n")
print("Last 2 rows:\n", weather_df.tail(2), "\n")
print("Statistical summary:\n", weather_df.describe(include="all"), "\n")

# ---------------------------------------------------------------
# 5️⃣ Perform data slicing by row position and by column name
# ---------------------------------------------------------------
print("Rows 5 to 8:\n", weather_df.iloc[5:9], "\n")
print("Columns: Temperature & Humidity:\n", weather_df[["Temperature (C)", "Humidity"]].head(), "\n")

# ---------------------------------------------------------------
# 6️⃣ Slice data using a boolean flags array and a data range
# ---------------------------------------------------------------
# Example: select all 'Clear' weather records
clear_mask = weather_df["Weather"] == "Clear"
print("Records where Weather is Clear:\n", weather_df[clear_mask].head(), "\n")

# Example: select temperatures between 10°C and 20°C
temp_range = weather_df[
    (weather_df["Temperature (C)"] >= 10) & (weather_df["Temperature (C)"] <= 20)
]
print("Records with temperature between 10°C and 20°C:\n", temp_range.head(), "\n")

# ---------------------------------------------------------------
# 7️⃣ Demonstrate duplicated, nunique, and drop_duplicates
# ---------------------------------------------------------------
print("Duplicate rows count:", weather_df.duplicated().sum())
print("Unique weather types:", weather_df["Weather"].nunique(), "\n")

clean_df = weather_df.drop_duplicates()
print("DataFrame after dropping duplicates:\n", clean_df.head(), "\n")

# ---------------------------------------------------------------
# 8️⃣ Apply pd.to_numeric and pd.to_datetime safely
# ---------------------------------------------------------------
weather_df["Temperature (C)"] = pd.to_numeric(weather_df["Temperature (C)"], errors="coerce")
weather_df["Time"] = pd.to_datetime(weather_df["Time"], errors="coerce")

print("Converted data types:\n", weather_df.dtypes, "\n")

# ---------------------------------------------------------------
# 9️⃣ Set default values for missing data using .apply()
# ---------------------------------------------------------------
def fill_weather(x):
    return x if pd.notna(x) else "Unknown"

weather_df["Weather"] = weather_df["Weather"].apply(fill_weather)
print("Weather column after filling missing data:\n", weather_df["Weather"].unique(), "\n")

# ---------------------------------------------------------------
# 🔟 Implement a data cleaning step using .pipe()
# ---------------------------------------------------------------
def clean_types(df):
    """Convert data types safely."""
    df["Temperature (C)"] = pd.to_numeric(df["Temperature (C)"], errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    return df

df_cleaned = weather_df.pipe(clean_types)
print("After cleaning pipeline:")
print("Data types:\n", df_cleaned.dtypes)
print("Missing values:\n", df_cleaned.isna().sum(), "\n")

# ---------------------------------------------------------------
# 1️⃣1️⃣ Utilize .pipe() with partial arguments (threshold example)
# ---------------------------------------------------------------
def drop_missing_cols(df, threshold):
    """Drop columns with missing ratio above threshold."""
    return df.loc[:, df.isnull().mean() < threshold]

df_threshold = df_cleaned.pipe(partial(drop_missing_cols, threshold=0.3))
print("Columns kept after applying missing-value threshold:\n", df_threshold.columns, "\n")

print("✅ All assignment tasks completed successfully!")
