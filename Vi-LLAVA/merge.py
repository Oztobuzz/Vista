import os
import json
import argparse

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--folder", type=str, required=True)
    args.add_argument("--output-filename", type=str, required=True)

    args = args.parse_args()

    folder = args.folder
    output_filename = args.output_filename

    files = sorted(os.listdir(folder))

    all_data = []

    for file in files:
        print("filename", file)
        
        data = json.load(open(os.path.join(folder, file)))

        all_data.extend(data)

    print("Total", len(all_data), "items")

    with open(output_filename, "w") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)


