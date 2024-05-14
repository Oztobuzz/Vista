from .normalization import normalization
import re

class ModifyingDocuments:
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