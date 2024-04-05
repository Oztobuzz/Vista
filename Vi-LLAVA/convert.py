import os
import json

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--subset", type=str, required=True)
    parser.add_argument("--caption-path", type=str, required=True, default=None)
    parser.add_argument("--instance-path", type=str, required=False, default=None)

    args = parser.parse_args()

    folder = args.folder
    subset = args.subset
    caption_path = args.caption_path
    instance_path = args.instance_path
    
    # Caption

    with open(caption_path, 'r') as f:
        caption_data = json.load(f)
    images = caption_data['images']
    annotations = caption_data['annotations']

    data = {}

    for image in images:
        id = image['id']
        file_name = image['file_name']
        coco_url = image['coco_url']
        height = image['height']
        width = image['width']
        date_capture = image['date_captured']
        flickr_url = image['flickr_url']

        data[id] = {
            "file_name": file_name,
            "coco_url": coco_url,
            "height": height,
            "width": width,
            "date_capture": date_capture,
            "flickr_url": flickr_url,
            "captions": [],
            "bboxes": []
        }

    for annotation in annotations:
        image_id = annotation['image_id']
        caption = annotation['caption']
        data[image_id]['captions'].append(caption)

    # Instance
    if instance_path is not None:
        with open(instance_path, 'r') as f:
            instance_data = json.load(f)
        
        instances = instance_data['annotations']
        categories = instance_data['categories']

        # with open(f'{folder}/categories.json', 'w', encoding='utf-8') as f:
        #     json.dump(categories, f, ensure_ascii=False, indent=4)

        for instance in instances:
            image_id = instance['image_id']
            bbox = instance['bbox']
            category_id = instance['category_id']
            data[image_id]['bboxes'].append({
                "bbox": bbox,
                "category_id": category_id
            })

        print(f'Process {len(data)} images, {len(instances)} instances, {len(annotations )} captions, {len(categories)} categories')

        with open(f'{folder}/{subset}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
