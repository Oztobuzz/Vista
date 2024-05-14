# Vista

![image/png](https://cdn-uploads.huggingface.co/production/uploads/630a5ef0e81e1dea2cedcec0/a9hcD8YWqlmsaEHvr2ole.png)

> "700.000 Vietnamese vision-language samples open-source dataset"

This dataset contains over 700,000 Vietnamese vision-language samples, created by Gemini Pro. We employed several prompt engineering techniques: few-shot learning, caption-based prompting and image-based prompting.

- For the COCO dataset, we generated data using Llava-style prompts
- For the ShareGPT4V dataset, we used translation prompts.

- *Caption-based prompting*: involves using accurate captions and bounding boxes from the original dataset.
- *Image-based prompting*: uses images to create captions and conversations.

Curation process involved removing any Han, Japanese, and Korean characters. The data was also refined by filtering out samples with high perplexity levels.

![image/png](https://cdn-uploads.huggingface.co/production/uploads/617296c180f98c89a18948d2/mhVuEEC08oNHss_sxgWiA.png)

![image/svg](https://huggingface.co/front/assets/huggingface_logo.svg) 

[HuggingFace Dataset](https://huggingface.co/datasets/Vi-VLM/Vista)

## Data process

### Vi-LLAVA

Follow the instructions in [Vi-LLAVA/](https://github.com/Oztobuzz/Vista/tree/main/Vi-LLAVA) folder.

### Translate ShareGPT4V
```bash
bash scripts/translate_shareGPT4V.sh
```

### WIT

Follow the instructions in [WIT/](https://github.com/Oztobuzz/Vista/tree/main/WIT) folder.

### Filtering perplexity
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Oztobuzz/Vista/blob/main/examples/filter_perplexity.ipynb)

``` python
from perplexity.filtering import FilteringPerplexity

# Specific your own dataset
datasets = load_dataset("Specific your dataset", split="train")

# Set up perplextiy filtering
perplexity_filtering = FilteringPerplexity(
    sentencepiece_model_path=os.path.join('path to sentencepiece model'),
    kenlm_model_path=os.path.join("path to kenlm model"),
)

# Compute perplexity
data_contains_perplex = perplexity_filtering.compute(dataset)

# Filter perplexity
threshold = 100  # Set your own threshold if needed
data_filtered = perplexity_filtering.filter(data_contains_perplex, threshold=threshold)
```