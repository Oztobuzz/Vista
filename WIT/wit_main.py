import multiprocessing
import os
import time
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import json
from tqdm import tqdm

import argparse

TIME_PER_REQUEST = 15

def run_query(system_message, query, image_url, model_name, max_output_tokens=16000, temperature=0.5):
    st_time = time.time()
    system_message += query
    if "http://" in image_url:
        image_url = image_url.replace("http://", "https://")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(image_url, stream=True, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error: Can not get image from url: {image_url}")
    img = Image.open(response.raw)

    if img is None:
        raise Exception(f"Error: Image not found {image_url}")

    model = genai.GenerativeModel(model_name)
    config = genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=max_output_tokens,
        temperature=temperature)
    
    response = model.generate_content(
        [system_message, img],
        safety_settings={
            'HARM_CATEGORY_HARASSMENT': 'block_none',
            'HARM_CATEGORY_HATE_SPEECH': 'block_none',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'
        },
        generation_config = config
    )
    response.resolve()
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

def process_func(process_idx, api_key, process_ids):
    print('API key:', api_key)
    print('Number of samples:', len(process_ids))
    genai.configure(api_key=api_key)

    # Load processed data
    os.makedirs(output_path, exist_ok=True)

    output_gen_path = f"{output_path}/{subset}_{process_idx}.json"

    if os.path.exists(output_gen_path):
        with open(output_gen_path, "r") as f:
            gen_data = json.load(f)
    else:
        gen_data = []

    cnt = 0

    for (i, id) in tqdm(process_ids):
        # if cnt >= 5:
        #     break
        if id in [sample["id"] for sample in gen_data]:
            continue
        
        sample = data[i]

        image_url = sample["image_url"]
        
        text_fields = [
            'page_title', 'section_title', 
            'hierarchical_section_title', 'caption_reference_description', 
            'caption_attribution_description', 'caption_alt_text_description',
            'context_page_description', 'context_section_description'
        ]

        texts = [sample[field] for field in text_fields if field in sample]
        texts = list(set(texts))
        
        extra_info = "\n".join([f"- {text}" for text in texts])

        query = \
        f"""
        # Input:
        Thông tin thêm:
        {extra_info}

        Đoạn hội thoại:

        """
        
        try:
            response = run_query(system_message, query, image_url, model_name, max_output_tokens, temperature)    
            conversation = parse_conversation(response)
            sample["conversation"] = conversation
            gen_data.append(sample)

            with open(output_gen_path, "w") as f:
                json.dump(gen_data, f, ensure_ascii=False, indent=4)

            cnt += 1
        except Exception as e:
            print(f"Process {process_idx}: Error at id {id}: {e}")
            time.sleep(TIME_PER_REQUEST)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--subset", type=str, required=True, default="train")
    parser.add_argument("--dataset-path", type=str, required=True, default="data/vi_wit_v1.train.filtered.json")
    parser.add_argument("--prompt-folder", type=str, required=True, default="prompts")
    parser.add_argument("--output-path", type=str, required=True, default="wit_output")
    parser.add_argument("--model-name", type=str, required=True, default="gemini-pro")
    parser.add_argument("--max-output-tokens", type=int, required=True, default=16000)
    parser.add_argument("--temperature", type=float, required=True, default=0.5)
    parser.add_argument("--api-key-path", type=str, default="api-key.txt")

    args = parser.parse_args()

    subset = args.subset
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

    # Load the dataset
    with open(dataset_path, "r") as f:
        data = json.load(f)

    processes = []

    ids = list(range(len(data)))

    for idx, api_key in enumerate(GOOGLE_API_KEYS):
        process_ids = [(i, data[i]['id']) for i in ids if i % len(GOOGLE_API_KEYS) == idx]
        process = multiprocessing.Process(target=process_func, args=(idx, api_key, process_ids))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()