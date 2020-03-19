import numpy as np

from data_utils.clean_text import clean_text
from data_utils.constants import (B_TOKEN, CHARACTER_SEPARATOR, CLASSES,
                                  I_TOKEN, SPLIT_TOKEN, TAGS,
                                  WORD_TAG_SEPARATOR)


def pad_sequences(seqs, lens, value=0):
    res = np.zeros([len(seqs), lens], dtype=np.int32)
    for i, seq in enumerate(seqs):
        res[i][:min(len(seq), lens)] = seq[:min(len(seq), lens)]
    return res


def transform_data(text, word_tokenizer, char_tokenizer):
    text, numbers = clean_text(text)
    words = text.split()
    n = iter(numbers)
    origin_words = [next(n).replace(' ', '') if x == '0' else (
        '\n' if x == '|' else x) for x in words]
    seq_len = len(words)
    chars = char_tokenizer.texts_to_sequences(words)
    words = word_tokenizer.texts_to_sequences([text])
    char_lens = [len(x) for x in chars]
    chars = pad_sequences(chars, max(char_lens))
    return words[0], seq_len, chars, char_lens, origin_words


if __name__ == '__main__':
    a = [[1], [1, 2], [3, 4, 5]]
    print(pad_sequences(a, 2))
