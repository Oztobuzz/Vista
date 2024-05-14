import re
import os
import json
import argparse

ranges = [
    {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
    {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
    {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
    {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
    {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
    {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
    {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
    {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
    {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
    {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
    {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
    {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
    {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

bbox_pattern = r'\[\d\.\d+, \d\.\d+, \d\.\d+, \d\.\d+\]'

def is_cjk(char):
    return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def has_cjk(word):
    return any([is_cjk(char) for char in word])

def has_bbox_format(text):
    matches = re.search(bbox_pattern, text)
    return bool(matches)

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--folder", type=str, required=True)
    args.add_argument("--output", type=str, required=True)

    args = args.parse_args()

    folder = args.folder
    output = args.output

    files = sorted(os.listdir(folder))

    cjk_cnt = 0
    
    bbox_cnt = 0

    removed_ids = []

    for file in files:
        print("filename", file)
        
        data = json.load(open(os.path.join(folder, file)))

        for item in data:
            id = item["id"]
            conversation = item["conversation"]
            for turn in conversation:
                content = turn["content"]

                flag = True

                if has_cjk(content):
                    print(f"id {id}", "Has cjk", content)
                    cjk_cnt += 1
                    flag = False

                if has_bbox_format(content):
                    print(f"id {id}", "Has bbox format", content)
                    bbox_cnt += 1
                    flag = False
                
                if flag == False:
                    removed_ids.append(id)
                
    
    print(f"Folder {folder}", "Total", cjk_cnt, "items have Chinese, Japanese, Korean characters (CJK)")
    print(f"Folder {folder}", "Total", bbox_cnt, "items have bbox format")


    if not os.path.exists(output):
        os.makedirs(output)

    for file in files:
        filtered_data = []

        data = json.load(open(os.path.join(folder, file)))

        for item in data:
            if item["id"] not in removed_ids:
                filtered_data.append(item)
        
        with open(os.path.join(output, file), 'w') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    