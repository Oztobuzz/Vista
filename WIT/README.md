## Download dataset

Download dataset that we extracted, filtered from WIT dataset from this link :[Link](https://drive.google.com/drive/folders/1SzlM2nXwT37h1mt63lTHSC1T_e9fjLeF?usp=sharing)

Extract and dataset placed in folders data/.

## Get Gemini API Keys

Create and place your Gemini API Keys in api-key.txt file.

## Gen script

```bash
bash gen.sh
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