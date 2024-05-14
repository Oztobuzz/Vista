from tqdm import tqdm
import sentencepiece
import kenlm
from datasets import Dataset
from .document_modification import ModifyingDocuments

class FilteringPerplexity:
    def __init__(self, sentencepiece_model_path, kenlm_model_path, num_proc=2):
        self.sentencepiece_model = load_sentencepiece_model(sentencepiece_model_path)
        self.kenlm_model = load_kenlm_model(kenlm_model_path)
        self.num_proc = num_proc

    def compute(self, dataset: Dataset, conversation_feature_name="conversation", content_feature_name="content"):
        dataset = dataset.map(
            lambda examples: self._compute_perplexity(
                examples, conversation_feature_name, content_feature_name
            ), num_proc=self.num_proc)
        return dataset
    
    @staticmethod
    def filter(dataset: Dataset, threshold):
        dataset = dataset.filter(lambda example: example["perplexity"] < threshold)
        return dataset

    def _compute_perplexity(self, example, conversation_feature_name="conversation", content_feature_name="content"):
        check_document = example[conversation_feature_name]
        score = self._compute_perplexity_score(
                check_document[-1][content_feature_name]
        )
        example["perplexity"] = score
        return example

    def _compute_perplexity_score(self, document):
        document = ModifyingDocuments.normalization(
            document=document,
            remove_non_printing_characters=True,
            strip=True,
            lower_case=False,
            uniform_whitespace=True,
            replace_digits_with_zeros=True,
            replace_unicode_punctuation=True,
        )
        document = ModifyingDocuments.tokenization(
            document, self.sentencepiece_model, join_on_whitespace=True
        )
        doc_log_score, doc_length = 0, 0
        for line in document.split("\n"):
            log_score = self.kenlm_model.score(line)
            length = len(line.split()) + 1
            doc_log_score += log_score
            doc_length += length
        pp_score = 10.0 ** (-doc_log_score / doc_length)
        pp_score = round(pp_score, 1)
        return pp_score

def load_sentencepiece_model(path_sentencepiece_model):
    sentencepiece_model = sentencepiece.SentencePieceProcessor()
    sentencepiece_model.load(path_sentencepiece_model)
    return sentencepiece_model
    
def load_kenlm_model(path_kenlm_model):
    return kenlm.Model(path_kenlm_model)
