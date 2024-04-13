import pandas as pd
import json

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-tsv", type=str, required=True)
    parser.add_argument("--output-json", type=str, required=True)

    args = parser.parse_args()

    input_tsv = args.input_tsv
    output_json = args.output_json

    df = pd.read_csv(input_tsv, sep="\t")

    df = df[df['language'] == 'vi']

    df = df.fillna("")

    data = df.to_dict('records')

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)