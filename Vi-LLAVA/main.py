import multiprocessing
import os
import time
import google.generativeai as genai
import json
from tqdm import tqdm

import argparse

TIME_PER_REQUEST = 8

def run_query(system_message, query, model_name, max_output_tokens=16000, temperature=0.5):
    system_message += query
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
    st_time = time.time()
    safety_settings = [ 
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}, 
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"}, 
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"}, 
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}, 
    ]
    response = chat.send_message(
        system_message, 
        safety_settings=safety_settings,
        generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=max_output_tokens,
        temperature=temperature)
    )
    end_time = time.time()
    if (end_time - st_time) < TIME_PER_REQUEST:
        time.sleep(TIME_PER_REQUEST - (end_time - st_time))
    else:
        time.sleep(1)
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

def process_func(i, api_key, process_ids):
    print('API key:', api_key)
    print('Number of samples:', len(process_ids))
    genai.configure(api_key=api_key)

    # Load processed data
    os.makedirs(output_path, exist_ok=True)

    output_gen_path = f"{output_path}/{task}_{i}.json"

    if os.path.exists(output_gen_path):
        with open(output_gen_path, "r") as f:
            gen_data = json.load(f)
    else:
        gen_data = []

    for id in tqdm(process_ids):
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
            query = parse_bboxes(query, bboxes, categories, width, height)
            query += "\nSuy luận phức tạp:\n"

        if task == "detail_description":
            query = f"\n\nMô tả:\n{captions_lines}\n\n"
            query = parse_bboxes(query, bboxes, categories, width, height)
            query += "\nMô tả chi tiết:\n"
        # print('Query:', query)
        try:
            response = run_query(system_message, query, model_name, max_output_tokens, temperature)
        
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

            with open(output_gen_path, "w") as f:
                json.dump(gen_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Process {i}: Error at id {id}: {e}")
            print('Check here')
            time.sleep(TIME_PER_REQUEST)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--task", type=str, required=True, 
        choices=["conversation", "complex_reasoning", "detail_description"]
    )
    parser.add_argument("--dataset-path", type=str, required=True, default="COCO2017/val.json")
    parser.add_argument("--prompt-folder", type=str, required=True, default="prompts/conversation")
    parser.add_argument("--output-path", type=str, required=True, default="conversation")
    parser.add_argument("--model-name", type=str, required=True, default="gemini-pro")
    parser.add_argument("--max-output-tokens", type=int, required=True, default=16000)
    parser.add_argument("--temperature", type=float, required=True, default=0.5)
    parser.add_argument("--api-key-path", type=str, default="api-key.txt")

    args = parser.parse_args()
    
    task = args.task
    dataset_path = args.dataset_path
    prompt_folder = args.prompt_folder
    output_path = args.output_path
    model_name = args.model_name
    max_output_tokens = args.max_output_tokens
    temperature = args.temperature
    api_key_path = args.api_key_path

    print("Arguments:", args)

    GOOGLE_API_KEYS = []

    # Load the API key
    with open(api_key_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            GOOGLE_API_KEYS.append(line.strip())

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

    with open("COCO2017/categories.json", "r") as f:
        categories = json.load(f)

    # Load the dataset
    with open(dataset_path, "r") as f:
        data = json.load(f)

    processes = []

    ids = data.keys()

    for idx, api_key in enumerate(GOOGLE_API_KEYS):
        process_ids = [id for i, id in enumerate(ids) if i % len(GOOGLE_API_KEYS) == idx]
        process = multiprocessing.Process(target=process_func, args=(idx, api_key, process_ids))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()