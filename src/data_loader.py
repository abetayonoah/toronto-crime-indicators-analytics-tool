import pandas as pd


# Load dataset
def load_data(file_path):

    try:

        df = pd.read_csv(file_path)

        return df

    except FileNotFoundError:

        print("File not found.")

        return None


# Preview dataset
def data_preview(df):

    return df.head()