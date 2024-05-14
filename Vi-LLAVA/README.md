## Install packages and libraries

```bash
pip install -r requirements.txt
```

## Download dataset

Download dataset from :[Link](https://drive.google.com/drive/folders/1brh6TFoUCtkfT0k4gexzE-KOdMs8KGw1?usp=sharing)

Extract and dataset placed in folders COCO2017/ and UIT-VilC/

## Get Gemini API Keys

Create and place your Gemini API Keys in api-key.txt file.

## Gen script

```bash
bash gen_conversation.sh
```

## Processing

We see that results from Gemini often have problems such as: 

- Containing Chinese, Japanese, and Korean characters; 

- Tasks that use bounding box information, bounding boxes are repeated.

So we use some of the filtering used in the preprocessing.py file.

Examples:

```bash
python preprocessing.py --folder train_conversation --output filtered_train_conversation
```