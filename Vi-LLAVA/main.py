import os
import google.generativeai as genai
import json

import argparse

GOOGLE_API_KEY="AIzaSyCKTDDSbBY-EMb9FO33YgV16JXHblFMpVA"

genai.configure(api_key=GOOGLE_API_KEY)

def run_query(system_message, query, max_output_tokens=16000, temperature=0.5):
    system_message += query
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(
        system_message, 
        safety_settings={
            'HARM_CATEGORY_HARASSMENT': 'block_none',
            'HARM_CATEGORY_HATE_SPEECH': 'block_none',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'
        }, 
        generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=max_output_tokens,
        temperature=temperature)
    )

    return response.text

def parse_conversation(response):
    turns = response.split("===")
    conversation = []
    for idx, turn in enumerate(turns):
        if idx % 2 == 0:
            conversation.append({
                "role": "user",
                "content": turn.replace("Câu hỏi:", "").strip()
            })
        else:
            conversation.append({
                "role": "assistant",
                "content": turn.replace("Trả lời:", "").strip()
            })
    return conversation

def parse_bboxes(query, bboxes, categories, width, height):
    for bbox in bboxes:
        category_id = bbox['category_id']
        category_name = [category for category in categories if category['id'] == category_id][0]['vi_name']
        x = bbox['bbox'][0] / width
        y = bbox['bbox'][1] / height
        w = bbox['bbox'][2] / width
        h = bbox['bbox'][3] / height
        query += f"{category_name}: [{x:.3f}, {y:.3f}, {w:.3f}, {h:.3f}]\n"
    return query

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--task", type=str, required=True, 
        choices=["conversation", "complex_reasoning", "detail_description"]
    )
    parser.add_argument("--dataset-path", type=str, required=True, default="COCO2017/val.json")
    parser.add_argument("--prompt-folder", type=str, required=True, default="prompts/conversation")
    parser.add_argument("--num-samples", type=int, required=True, default=10)
    parser.add_argument("--output-path", type=str, required=True, default="conversation.json")
    parser.add_argument("--max-output-tokens", type=int, required=True, default=16000)
    parser.add_argument("--temperature", type=float, required=True, default=0.5)

    args = parser.parse_args()
    
    task = args.task
    dataset_path = args.dataset_path
    prompt_folder = args.prompt_folder
    num_samples = args.num_samples
    output_path = args.output_path
    max_output_tokens = args.max_output_tokens
    temperature = args.temperature

    # Load the system message
    with open(f"{prompt_folder}/system_message.txt", "r") as f:
        system_message = f.read()
        system_message = system_message.strip()

    # Load the conversation
    N = 2

    for i in range(N):
        with open(f"{prompt_folder}/{i:03d}_caps.txt", "r") as f:
            cap = f.read().strip()

        with open(f"{prompt_folder}/{i:03d}_conv.txt", "r") as f:
            conv = f.read().strip()
        if task == "conversation":
            system_message += f"\n\nMô tả:\n{cap}\n\nCác đoạn hội thoại:\n{conv}"
        if task == "complex_reasoning":
            system_message += f"\n\nMô tả:\n{cap}\n\nSuy luận phức tạp:\n{conv}"
        if task == "detail_description":
            system_message += f"\n\nMô tả:\n{cap}\n\nMô tả chi tiết:\n{conv}"

    # Load the dataset
    with open(dataset_path, "r") as f:
        data = json.load(f)

    # Load processed data
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            gen_data = json.load(f)
    else:
        gen_data = []

    cnt = 0

    with open("COCO2017/categories.json", "r") as f:
        categories = json.load(f)

    for id in data.keys():
        if id in [sample["id"] for sample in gen_data]:
            continue
        
        sample = data[id]

        file_name = sample['file_name']
        coco_url = sample['coco_url']
        height = sample['height']
        width = sample['width']
        date_capture = sample['date_capture']
        flickr_url = sample['flickr_url']

        captions = sample['captions']
        captions_lines = "\n".join(captions)

        bboxes = sample["bboxes"]
        
        if task == "conversation":
            query = f"\n\nMô tả:\n{captions_lines}\nĐoạn hội thoại:\n"

        if task == "complex_reasoning":
            query = f"\n\nMô tả:\n{captions_lines}\n\n"
            parse_bboxes(query, bboxes, categories, width, height)
            query += "\nSuy luận phức tạp:\n"

        if task == "detail_description":
            query = f"\n\nMô tả:\n{captions_lines}\n\n"
            parse_bboxes(query, bboxes, categories, width, height)
            query += "\nMô tả chi tiết:\n"

        response = run_query(system_message, query, max_output_tokens, temperature)
        
        if task in ["conversation", "complex_reasoning"]:
            conversation = parse_conversation(response)

        if task == "detail_description":
            conversation = [
                {
                    "role": "user",
                    "content": "Mô tả chi tiết của hình ảnh"
                },
                {
                    "role": "assistant",
                    "content": response
                }
            ]

        gen_data.append({
            "id": id,
            "file_name": file_name,
            "coco_url": coco_url,
            "height": height,
            "width": width,
            "date_capture": date_capture,
            "flickr_url": flickr_url,
            "captions": captions,
            "conversation": conversation
        })

        with open(output_path, "w") as f:
            json.dump(gen_data, f, ensure_ascii=False, indent=4)

        cnt += 1
        if cnt == num_samples:
            break