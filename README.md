# Vista

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