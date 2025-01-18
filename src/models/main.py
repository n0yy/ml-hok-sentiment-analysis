import os
import time
import pandas as pd
from bert.model import IndoBERTForSentimentAnalysis

if __name__ == "__main__":
    model = IndoBERTForSentimentAnalysis()
    files = os.listdir("data/processed")
    start = time.time()

    for file in files:
        df = pd.read_csv(f"data/processed/{file}")
        print(f"============================== Analyzing in Dataframe {file} ==============================")
        result_df = model.analyze_dataframe(df=df, X="comment_prep", batch_size=32)
        # Save to analyzed folder
        result_df.to_csv(f"data/analyzed/{file}", index=False)
        
    end = time.time()
    print(f"Total time: {(end - start) / 60} minutes")
    