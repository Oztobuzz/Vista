import google.generativeai as genai
import os
import time
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
import asyncio
from datasets import Dataset


def run_query(query, max_output_tokens=16000, temperature=0.5):
    system_message = ""
    system_message += query
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    try:
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
    except Exception as e:
        print(e)
    return response.text

async def main():
  list_of_conversations = []
  for conv in tqdm(en_conversations[:10]):
    genai.configure(api_key="AIzaSyAzlrIU2nXzO8Ch60zo6Anr6dH2gwZTs9U")
    msgs = [x['value'] for x in conv]
    
    list_of_prompts = []
    for msg in msgs:  
      prompt = f"""Please translate the following English string to Vietnamese, preserving the same format, output just the string:
    English string: {msg}
    Translate to Vietnamese:"""
      list_of_prompts.append(prompt)
    try:
        
      tasks = []
      async with asyncio.TaskGroup() as tg:
        for i in range(len(list_of_prompts)):
          run_query_async = asyncio.to_thread(run_query, list_of_prompts[i])
          task = tg.create_task(run_query_async)
          
          try:
            res = await asyncio.shield(task)
          except Exception as e :
            print(e)
          tasks.append(res)
        
      list_of_conversations.append(tasks)
    
    except Exception as e:
      print(e)
      
  return list_of_conversations 

    
if __name__ == '__main__':
    dataset = load_dataset("Lin-Chen/ShareGPT4V", 'ShareGPT4V')

    en_conversations = dataset["train"]['conversations']
    ids = dataset["train"]['id']
    images = dataset["train"]['image']
    list_of_conversations = asyncio.run(main())
    
    vi_conversations = []
    for i, conv in enumerate(en_conversations[:10]):
        for j, msg in enumerate(conv):
            msg['value'] = list_of_conversations[i][j]
        vi_conversations.append(conv)
        
        
    dataset_dict = {"id": [], "image": [], "en_conversations": [], "vi_conversations": []}
    
    for i in range(0, len(vi_conversations)):
        image =  dataset["train"][i]['image']
        en_conversations = dataset["train"][i]['conversations']
        img_id =  dataset["train"][i]['id']
        image =  dataset["train"][i]['image']
        
        dataset_dict['en_conversations'].append(en_conversations) 
        dataset_dict['vi_conversations'].append(vi_conversations[i]) 
        dataset_dict['image'].append(image) 
        dataset_dict['id'].append(img_id) 

    vi_dataset = Dataset.from_dict(dataset_dict)
    vi_dataset.push_to_hub("Oztobuzz/Vi_ShareGPT4V")