import pandas as pd
from fetch_bazaar import fetch_bazaar, clean_data

def export(path_csv="bazaar_data.csv",
           path_xlsx="bazaar_data.xlsx"):
    df = clean_data(fetch_bazaar())

    # Add a rank column by margin
    df["flip_rank"] = df["margin"].rank(ascending=False).astype(int)

    df.to_csv(path_csv, index=False)
    df.to_excel(path_xlsx, index=False)
    print(f"Exported {len(df)} rows → {path_csv} + {path_xlsx}")
    return df

if __name__ == "__main__":
    export()