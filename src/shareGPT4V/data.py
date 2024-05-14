from tqdm import tqdm
from .model_service import GeminiClient
from datasets import Dataset

client = GeminiClient

def translate_to_vi(batch_vi_conversation):
    list_of_conversations_vi = []
    for conversation in tqdm(batch_vi_conversation):
        messages = [x['value'] for x in conversation]

        translate_prompts = get_translate_prompts(messages)
        try:            
            translated_messages = []
            for request_translate_prompt in translate_prompts:
                translated_message = client.query(request_translate_prompt)
                translated_messages.append(translated_message)
              
            list_of_conversations_vi.append(translated_messages)

        except Exception as e:
            list_of_conversations_vi = []
            break
    return list_of_conversations_vi 

def get_translate_prompts(messages):
      translate_prompts = []
      for message in messages:  
          prompt = f"""Please translate the following English string to Vietnamese, preserving the same format, output just the string:
  English string: {message}
  Translate to Vietnamese:"""
          translate_prompts.append(prompt)
      return translate_prompts

def push_data_to_hub(data_dict):
    try:
        first_id = data_dict['id'][0]
        print(f"Pushing {first_id} to HF")
        vi_dataset = Dataset.from_dict(data_dict)
        vi_dataset.push_to_hub("Oztobuzz/Processed_Vi_ShareGPT4V", f'start_from_{first_id}', data_dir=f"data/start_from_{first_id}")
    except Exception as e:
        print(e)
