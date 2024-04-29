import pyreadstat
import pandas as pd


def save_bigdf():
    # def save_bigdf():
    data_path = r"C:\\Users\\justi\\Dropbox\\Work\\Job Search\\Other\\GSS\\GSS_sas\\gss7222_r3.sas7bdat"
    df, meta = pyreadstat.read_sas7bdat(data_path)

    # Split the DataFrame into two parts
    num_rows = len(df)
    half_rows = num_rows // 2

    df_part1 = df.iloc[:half_rows]
    df_part2 = df.iloc[half_rows:]

    # Save each part as a separate Parquet file
    part1_output_path = "gss_data_part1.parquet"
    part2_output_path = "gss_data_part2.parquet"

    df_part1.to_parquet(part1_output_path)
    df_part2.to_parquet(part2_output_path)

    print(f"DataFrame split and saved as '{part1_output_path}' and '{part2_output_path}'")

def get_bigdf():
    part1_output_path = "gss_data_part1.parquet"
    part2_output_path = "gss_data_part2.parquet"
    # Read the Parquet files back into DataFrames
    df_part1 = pd.read_parquet(part1_output_path)
    df_part2 = pd.read_parquet(part2_output_path)

    # Concatenate the two parts back into a single DataFrame
    df_combined = pd.concat([df_part1, df_part2], ignore_index=True)

    print("DataFrame parts combined back into a single DataFrame.")

if __name__ == "__main__":
    print("hi")
    # save_bigdf()
    get_bigdf()
