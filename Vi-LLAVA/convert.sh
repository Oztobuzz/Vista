## UIT-VilC
python convert.py \
    --folder UIT-ViIC \
    --subset train \
    --caption-path UIT-ViIC/uitviic_captions_train2017.json

python convert.py \
    --folder UIT-ViIC \
    --subset val \
    --caption-path UIT-ViIC/uitviic_captions_val2017.json

python convert.py \
    --folder UIT-ViIC \
    --subset test \
    --caption-path UIT-ViIC/uitviic_captions_test2017.json

## COCO2017

python convert.py \
    --folder COCO2017 \
    --subset train \
    --caption-path COCO2017/captions_train2017_trans.json \
    --instance-path COCO2017/instances_train2017.json

python convert.py \
    --folder COCO2017 \
    --subset val \
    --caption-path COCO2017/captions_val2017_trans.json \
    --instance-path COCO2017/instances_val2017.json