import os
import pandas as pd
from conf import OUTPUT_DIR, INDEX_DIR
from pathlib import Path
import glob
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, KEYWORD, STORED


def parse_documents(writer, p_df):
    # Iterate over parquet and add documents to writer
    for index, row in p_df.iterrows():
        # "subject_id", "predicate", "object"
        # print(str(row))
        if row["predicate"] == "type":
            writer.add_document(
                id=row["subject_id"],
                predicate=row["predicate"],
                type=row["object"].replace(".", ","),
            )

        if row["predicate"] == "name":

            writer.add_document(
                id=row["subject_id"], predicate=row["predicate"], name=row["object"]
            )

        if row["predicate"] == "alias":
            writer.add_document(
                id=row["subject_id"], predicate=row["predicate"], alias=row["object"]
            )


# Get files from folder
def get_files():
    if os.path.exists(OUTPUT_DIR):
        parquet_files = []
        for file in os.listdir(OUTPUT_DIR):
            if file.endswith(".parquet"):
                parquet_files.append(file)
        return parquet_files


# Get one large DF
def get_concat_df():
    data_dir = Path(OUTPUT_DIR)
    full_df = pd.concat(
        pd.read_parquet(parquet_file) for parquet_file in data_dir.glob("*.parquet")
    )
    return full_df


# If directory is not empty or not created create
def clear_directory(path):
    if os.path.exists(path):
        files = glob.glob(path + "/*")
        for f in files:
            os.remove(f)
        return True
    else:
        os.mkdir(path)


if __name__ == "__main__":
    # Get concaternated parquet pandas dataframe
    parquet_df = get_concat_df()

    # Schema for indexing
    input_data_schema = Schema(
        id=ID(stored=True),
        predicate=STORED(),
        name=TEXT(stored=True),
        alias=TEXT(stored=True),
        type=KEYWORD(stored=True),
    )

    # Clear index directory
    clear_directory(INDEX_DIR)

    i = index.create_in(INDEX_DIR, input_data_schema)
    w = i.writer()

    # Add documents to index
    parse_documents(w, parquet_df)

    # Commit changes to index and save it to output folder
    w.commit()
