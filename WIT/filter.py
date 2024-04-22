import os
import json
import hashlib  

DATA_PATH = 'data/'

SUBSET = "test"

MIN_HEIGHT = 336
MIN_WIDTH = 336

ALLOWED_EXTENSIONS = ['image/jpeg', 'image/png']

data = []

for i in range(5):
    with open(DATA_PATH + f'vi_wit_v1.{SUBSET}.all-{i:05d}-of-00005.json', 'r') as f:
        data_ = json.load(f)
    
    data.extend(data_)

n_remove_resolution = 0
for i, sample in enumerate(data):
    if sample['original_height'] < MIN_HEIGHT or sample['original_width'] < MIN_WIDTH:
        n_remove_resolution += 1

n_remove_extension = 0
for i, sample in enumerate(data):
    if sample['mime_type'] not in ALLOWED_EXTENSIONS:
        n_remove_extension += 1

print('Remove resolution samples percentage:', n_remove_resolution / len(data) * 100)
print('Remove extension samples percentage:', n_remove_extension / len(data) * 100)


filtered_data = []

for i, sample in enumerate(data):
    if sample['original_height'] < MIN_HEIGHT or sample['original_width'] < MIN_WIDTH:
        continue
    if sample['mime_type'] not in ALLOWED_EXTENSIONS:
        continue
    image_url = sample['image_url']
    m = hashlib.md5()
    m.update(image_url.encode("utf-8"))
    sample['id'] = str(int(m.hexdigest(), 16))[0:12]
    filtered_data.append(sample)

print('Number of samples:', len(filtered_data))

with open(DATA_PATH + f'vi_wit_v1.{SUBSET}.filtered.json', 'w') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)