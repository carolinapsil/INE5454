import pandas as pd

from src.billboard import extract_billboard_charts
from src.official_charts import extract_official_charts

if __name__ == '__main__':
    df_billboard = extract_billboard_charts()
    df_official_charts = extract_official_charts()

    df_final = pd.concat([df_billboard, df_official_charts], ignore_index=True)

    df_final.to_json('generated/charts.json', orient='records', indent=2)
