import pandas as pd
import os
from tqdm.auto import tqdm
from preprocessor.preprocessor import Preprocessor


if __name__ == "__main__":
    files = os.listdir("data/raw")
    preprocessor = Preprocessor()

    for file in tqdm(files, desc="Preprocess Data"):
        df = pd.read_csv(f"data/raw/{file}")
        df["comment_prep"] = df["comment"].apply(lambda x: preprocessor.fit(x, concate=True))
        print(f"============================== Preprocessed {file} ==============================")
        print(df.head())
        # Save to preprocessed folder
        df.to_csv(f"data/processed/{file}", index=False)