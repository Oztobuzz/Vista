from collections import defaultdict
from datasets import load_dataset
from .data import load_vi_and_en_field, translate_to_vi, push_data_to_hub

def check_existence_id(vi_dataset, en_dataset):
    existed_vi_ids = vi_dataset["train"]['id']
    not_existed_vi_conversations = [x for x in en_dataset["train"] if x['id'] not in existed_vi_ids]  
    print(f'number of not_existed_vi_conversations: {len(not_existed_vi_conversations)}')
    
    # Start from index 0
    not_existed_vi_conversations = not_existed_vi_conversations[0:4500] 
    print(f'number of not_existed_vi_conversations: {len(not_existed_vi_conversations)}')
    return not_existed_vi_conversations

def process_conversations(not_existed_vi_conversations, steps=100):
    current_data_dict = defaultdict(list)
    for step_num in range(0, len(not_existed_vi_conversations), steps):
        print(f"Processing from step {step_num} ...")
        try:
            batch_vi_conversation = get_batch_conversation(step_num, steps)
            vi_conversations = translate_to_vi(batch_vi_conversation)
            if(len(vi_conversations) == 0):
                print(f"Step {step_num} is error, will move to next step")
                continue
            current_data_dict: dict = extract_info(batch_vi_conversation, current_data_dict)

            # Upload to hub every 100 samples
            if (step_num % 100 == 0):
                push_data_to_hub(current_data_dict)
                current_data_dict = defaultdict(list)

        except Exception as e:
            print(e)
            continue

def get_batch_conversation(current_step, batch_num):
    batch_vi_samples = not_existed_vi_conversations[current_step:current_step+batch_num]
    batch_vi_conversation = [sample for sample in batch_vi_samples['conversations']]
    return batch_vi_conversation

def extract_info(batch_vi_conversation, current_data_dict) -> dict:
    for vi_conver_sample in batch_vi_conversation:
        current_data_dict['en_conversations'].append(vi_conver_sample['conversations']) 
        current_data_dict['vi_conversations'].append(vi_conver_sample) 
        current_data_dict['image'].append(vi_conver_sample['image']) 
        current_data_dict['id'].append(vi_conver_sample['id'])
    return current_data_dict

def load_vi_and_en_field():
    en_dataset = load_dataset("Lin-Chen/ShareGPT4V", 'ShareGPT4V')
    vi_dataset =  load_dataset("Oztobuzz/Processed_Vi_ShareGPT4V", 'default')
    return en_dataset, vi_dataset

if __name__ == "__main__":
    step = 100
    en_dataset, vi_dataset = load_vi_and_en_field()
    not_existed_vi_conversations = check_existence_id(en_dataset, vi_dataset)
    process_conversations(not_existed_vi_conversations, steps=step)