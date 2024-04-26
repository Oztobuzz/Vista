# Conversation
python main.py \
    --task conversation \
    --dataset-path COCO2017/train.json \
    --prompt-folder prompts/conversation \
    --output-path train_conversation \
    --model-name gemini-1.0-pro-latest \
    --max-output-tokens 16000 \
    --temperature 0.8 \
    --api-key-path api-key-1.txt

# Complex reasoning

python main.py \
    --task complex_reasoning \
    --dataset-path COCO2017/train.json \
    --prompt-folder prompts/complex_reasoning \
    --output-path train_complex_reasoning \
    --model-name gemini-1.0-pro-latest \
    --max-output-tokens 16000 \
    --temperature 0.8 \
    --api-key-path api-key-2.txt

# Detail Description

python main.py \
    --task detail_description \
    --dataset-path COCO2017/train.json \
    --prompt-folder prompts/detail_description \
    --output-path train_detail_description \
    --model-name gemini-1.0-pro-latest  \
    --max-output-tokens 16000 \
    --temperature 0.8 \
    --api-key-path api-key-2.txt