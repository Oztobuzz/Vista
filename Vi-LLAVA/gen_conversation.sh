# Conversation
python main.py \
    --task conversation \
    --dataset-path COCO2017/val.json \
    --prompt-folder prompts/conversation \
    --output-path conversation \
    --max-output-tokens 16000 \
    --temperature 0.8

# Complex reasoning

python main.py \
    --task complex_reasoning \
    --dataset-path COCO2017/val.json \
    --prompt-folder prompts/complex_reasoning \
    --output-path complex_reasoning \
    --max-output-tokens 16000 \
    --temperature 0.8

# Detail Description

python main.py \
    --task detail_description \
    --dataset-path COCO2017/val.json \
    --prompt-folder prompts/detail_description \
    --output-path detail_description \
    --max-output-tokens 16000 \
    --temperature 0.8