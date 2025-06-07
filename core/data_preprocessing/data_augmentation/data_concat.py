import pandas as pd

class DataConcat:
    def __init__(self, df1_path: str, df2_path: str):
        self.df1_path = df1_path
        self.df2_path = df2_path

    def load_data(self):
        self.df1 = pd.read_csv(self.df1_path)
        self.df2 = pd.read_csv(self.df2_path)

    def filter_and_merge(self) -> pd.DataFrame:
        # Step 1: Remove rows in df2 where input == raw_sentence in df1
        df2_filtered = self.df2[~self.df2["input"].isin(self.df1["raw_sentence"])].copy()

        # Step 2: Select and rename necessary columns
        df1_subset = self.df1[["input", "output", "tag"]].copy()
        df1_subset.rename(columns={"tag": "tags"}, inplace=True)
        df1_subset["tagged_sentence"] = pd.NA

        df2_subset = df2_filtered[["input", "s_output", "final_tags", "gpt_tagged_sentence", "tagged_sentence"]].copy()
        df2_subset.rename(columns={"s_output": "output", "final_tags": "tags"}, inplace=True)

        # Prefer gpt_tagged_sentence if not null, else tagged_sentence
        df2_subset["tagged_sentence"] = df2_subset["gpt_tagged_sentence"].fillna(df2_subset["tagged_sentence"])
        df2_subset = df2_subset[["input", "output", "tags", "tagged_sentence"]]

        # Concatenate and shuffle
        merged_df = pd.concat([df1_subset, df2_subset], ignore_index=True)
        merged_df = merged_df.sample(frac=1).reset_index(drop=True)  # Shuffle

        return merged_df

    def concat_data(self, output_path: str = None) -> pd.DataFrame:
        self.load_data()
        merged_df = self.filter_and_merge()
        if output_path:
            merged_df.to_csv(output_path, index=False)
        return merged_df
      
if __name__ == "__main__":
  df1_path = "/data/datnt3/text-normalization/data_storage/train_test/augment/2025-06-07/augmented_train_data.csv"
  df2_path = "/data/datnt3/text-normalization/data_storage/train_test/2025-05-25/train_data.csv"
  data_concat = DataConcat(df1_path=df1_path, df2_path=df2_path)
  merged_df = data_concat.concat_data(output_path="/data/datnt3/text-normalization/data_storage/train_test/2025-06-07/augmented_train_data.csv")
