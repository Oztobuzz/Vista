from .normalization import normalization
import re

class ModifyingDocuments:
    # @staticmethod
    # def remove_empty_el_from_list(list_):
    #     return [el for el in list_ if el]

    @staticmethod
    def remove_non_printing_characters(document, non_printing_characters_re):
        return non_printing_characters_re.sub("", document)

    @staticmethod
    def uniform_whitespace(
        document,
        whitespace=[
            " ",
            " ",
            " ",
            " ",
            " ",
            "　",
            " ",
            " ",
            " ",
            " ",
            "￼",
            "",
        ],
    ):
        """There are different whitespace characters."""
        whitespace = set(whitespace)
        document = "".join(
            [char if char not in whitespace else " " for char in document]
        )
        return document

    @staticmethod
    def replace_digits_with_zeros(document, digits_re):
        return digits_re.sub("0", document)

    @staticmethod
    def replace_unicode_punctuation(document, unicode_punctuation):
        return "".join(unicode_punctuation.get(c, c) for c in document)

    @staticmethod
    def normalization(
        document,
        remove_non_printing_characters,
        strip,
        lower_case,
        uniform_whitespace,
        replace_digits_with_zeros,
        replace_unicode_punctuation,
        non_printing_characters_re=normalization["non_printing_characters_re"],
        digits_re=normalization["digits_re"],
        unicode_punctuation=normalization["unicode_punctuation"],
    ):
        if remove_non_printing_characters:
            document = ModifyingDocuments.remove_non_printing_characters(
                document, non_printing_characters_re
            )
        if strip:
            document = document.strip()
        if not document:
            return document
        if lower_case:
            document = document.lower()
        if uniform_whitespace:
            document = ModifyingDocuments.uniform_whitespace(document)
        if replace_digits_with_zeros:
            document = ModifyingDocuments.replace_digits_with_zeros(document, digits_re)
        if replace_unicode_punctuation:
            document = ModifyingDocuments.replace_unicode_punctuation(
                document, unicode_punctuation
            )
        return document

    @staticmethod
    def tokenization(document, sentencepiece_model, join_on_whitespace):
        document_tokenized = sentencepiece_model.encode_as_pieces(document)
        if join_on_whitespace:
            document_tokenized = " ".join(document_tokenized)
        return document_tokenized

    # @staticmethod
    # def split_on_whitespace(
    #     document,
    #     new_line=False,
    #     tab=False,
    # ):
    #     """This method also removes concatenated spaces."""
    #     sep = [" "] + new_line * ["\n"] + tab * ["\t"]
    #     sep = "|".join(sep)
    #     split_document = re.split(sep, document)
    #     split_document = ModifyingDocuments.remove_empty_el_from_list(split_document)
    #     return split_document

    # @staticmethod
    # def strip(document, strip_characters):
    #     """Way faster than document.strip(strip_characters)
    #     since strip_characters is now a set instead of a str,
    #     and it contains a lot of elements (all the emojis)."""
    #     if not document:
    #         return document
    #     beg_ind = 0
    #     end_ind = len(document)
    #     for i in range(len(document)):
    #         if document[i] in strip_characters:
    #             beg_ind += 1
    #         else:
    #             break
    #     for i in range(1, len(document) + 1):
    #         if document[-i] in strip_characters:
    #             end_ind -= 1
    #         else:
    #             break
    #     document_stripped = document[beg_ind:end_ind]
    #     return document_stripped

    # @staticmethod
    # def get_words_from_document(
    #     document, sentencepiece_model_tok, lower_case, strip_characters
    # ):
    #     """Get words from a document. Non-reversible since the document
    #     is split on multiple characters, words are stripped of
    #     special characters and characters are converted to lower case.
    #     Useful to compute ratios, like the stopwords ratio."""
    #     if sentencepiece_model_tok:
    #         document_normalized = ModifyingDocuments.normalization(
    #             document=document,
    #             remove_non_printing_characters=True,
    #             strip=True,
    #             lower_case=True,
    #             uniform_whitespace=True,
    #             replace_digits_with_zeros=True,
    #             replace_unicode_punctuation=True,
    #         )
    #         words = ModifyingDocuments.tokenization(
    #             document_normalized, sentencepiece_model_tok, join_on_whitespace=False
    #         )
    #     else:
    #         words = ModifyingDocuments.split_on_whitespace(
    #             document, new_line=True, tab=True
    #         )
    #     if lower_case:
    #         words = [word.lower() for word in words]
    #     if strip_characters:
    #         words = [ModifyingDocuments.strip(word, strip_characters) for word in words]
    #         words = ModifyingDocuments.remove_empty_el_from_list(words)
    #     return words

    # @staticmethod
    # def words_augmentation(words, group_size, join_char):
    #     """Augment words, especially for Chinese (without a space between words)
    #     and Vietnamese (with a space between syllables)."""
    #     augmentation = [
    #         join_char.join(words[i: i + group_size])
    #         for i in range(len(words) - group_size + 1)
    #     ]
    #     return augmentation

    # @staticmethod
    # def split_on_newline_tab_whitespace(document):
    #     """First split on "\n", then on "\t", then on " "."""
    #     sentences = document.split("\n")
    #     sentences = [sentence.split("\t") for sentence in sentences]
    #     sentences = [
    #         [
    #             ModifyingDocuments.split_on_whitespace(subsentence)
    #             for subsentence in sentence
    #         ]
    #         for sentence in sentences
    #     ]
    #     return sentences

    # @staticmethod
    # def merge_on_whitespace_tab_newline(sentences):
    #     """Invert the method split_on_newline_tab_whitespace.
    #     Removes concatenated separators."""
    #     sentences = [
    #         [" ".join(subsentence) for subsentence in sentence if subsentence]
    #         for sentence in sentences
    #     ]
    #     sentences = ["\t".join(sentence) for sentence in sentences if sentence]
    #     if not sentences:
    #         return ""
    #     document = "\n".join(sentences)
    #     return document

    # @staticmethod
    # def should_keep_word_with_incorrect_substrings(
    #     word, strip_characters, incorrect_word_substrings
    # ):
    #     word = ModifyingDocuments.strip(word, strip_characters)
    #     should_keep = all(
    #         [(i_substr not in word) for i_substr in incorrect_word_substrings]
    #     )
    #     return should_keep

    # @staticmethod
    # def remove_words_with_incorrect_substrings(
    #     document,
    #     strip_characters,
    #     incorrect_word_substrings,
    # ):
    #     sentences = ModifyingDocuments.split_on_newline_tab_whitespace(document)
    #     sentences = [
    #         [
    #             [
    #                 word
    #                 for word in subsentence
    #                 if ModifyingDocuments.should_keep_word_with_incorrect_substrings(
    #                     word, strip_characters, incorrect_word_substrings
    #                 )
    #             ]
    #             for subsentence in sentence
    #         ]
    #         for sentence in sentences
    #     ]
    #     document = ModifyingDocuments.merge_on_whitespace_tab_newline(sentences)
    #     return document

    # @staticmethod
    # def should_keep_long_word(word, strip_characters, length_word_max_cutoff):
    #     """If the word is too long, but it contains only one
    #     special character, it might be a concatenation of one word,
    #     a punctuation, and another word, with no space between them.
    #     In this case, we give the word a pass."""
    #     if len(word) <= length_word_max_cutoff:
    #         return True
    #     word = ModifyingDocuments.strip(word, strip_characters)
    #     if not word:  # The word consisted only of strip characters
    #         return False
    #     if len(word) <= length_word_max_cutoff:
    #         return True
    #     return False

    # @staticmethod
    # def remove_long_words(
    #     document,
    #     strip_characters,
    #     length_word_max_cutoff,
    # ):
    #     sentences = ModifyingDocuments.split_on_newline_tab_whitespace(document)
    #     sentences = [
    #         [
    #             [
    #                 word
    #                 for word in subsentence
    #                 if ModifyingDocuments.should_keep_long_word(
    #                     word,
    #                     strip_characters,
    #                     length_word_max_cutoff,
    #                 )
    #             ]
    #             for subsentence in sentence
    #         ]
    #         for sentence in sentences
    #     ]
    #     document = ModifyingDocuments.merge_on_whitespace_tab_newline(sentences)
    #     return document

    # @staticmethod
    # def modifying_documents(
    #     document,
    #     cond_uniform_whitespace,
    #     cond_replace_unicode_punctuation,
    #     cond_remove_words_with_incorrect_substrings,
    #     strip_characters,
    #     incorrect_word_substrings,
    #     cond_remove_long_words,
    #     length_word_max_cutoff,
    # ):
    #     document = ModifyingDocuments.normalization(
    #         document=document,
    #         remove_non_printing_characters=False,
    #         strip=True,
    #         lower_case=False,
    #         uniform_whitespace=cond_uniform_whitespace,
    #         replace_digits_with_zeros=False,
    #         replace_unicode_punctuation=cond_replace_unicode_punctuation,
    #     )
    #     if cond_remove_words_with_incorrect_substrings:
    #         document = ModifyingDocuments.remove_words_with_incorrect_substrings(
    #             document,
    #             strip_characters,
    #             incorrect_word_substrings,
    #         )
    #     if cond_remove_long_words:
    #         document = ModifyingDocuments.remove_long_words(
    #             document,
    #             strip_characters,
    #             length_word_max_cutoff,
    #         )
    #     return document

