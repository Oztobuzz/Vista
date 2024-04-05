# Conversation
python main.py \
    --task conversation \
    --dataset-path COCO2017/val.json \
    --prompt-folder prompts/conversation \
    --num-samples 10 \
    --output-path conversation.json \
    --max-output-tokens 16000 \
    --temperature 0.8

# Complex reasoning

python main.py \
    --task complex_reasoning \
    --dataset-path COCO2017/val.json \
    --prompt-folder prompts/complex_reasoning \
    --num-samples 10 \
    --output-path complex_reasoning.json \
    --max-output-tokens 16000 \
    --temperature 0.8

# Detail Description

python main.py \
    --task detail_description \
    --dataset-path COCO2017/val.json \
    --prompt-folder prompts/detail_description \
    --num-samples 10 \
    --output-path detail_description.json \
    --max-output-tokens 16000 \
    --temperature 0.8