python wit_main.py \
    --subset train \
    --dataset-path data/vi_wit_v1.train.filtered.json \
    --prompt-folder prompts \
    --output-path wit_output \
    --model-name models/gemini-1.0-pro-vision-latest \
    --max-output-tokens 16000 \
    --temperature 0.0 \
    --api-key-path api-key.txt