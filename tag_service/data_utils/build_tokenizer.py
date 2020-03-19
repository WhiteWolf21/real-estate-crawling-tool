if __name__ == '__main__':
    import tensorflow as tf
    import re
    import pickle
    from data_utils.constants import ALL_TEXTS
    from keras.preprocessing.text import Tokenizer
    with open(ALL_TEXTS, 'r') as file:
        word_tokenizer = Tokenizer(
            filters='\t\n', lower=True, oov_token='<UNK>'
        )
        lines = file.readlines()
        word_tokenizer.fit_on_texts(lines)
        word_tokenizer.num_words = len(
            [x for x in word_tokenizer.word_counts.values() if x >= 5]) + 1
        word_tokenizer.word_index = dict(
            (k, v) for k, v in word_tokenizer.word_index.items() if v < word_tokenizer.num_words)
        word_tokenizer.word_index[word_tokenizer.oov_token] = word_tokenizer.num_words
        print(word_tokenizer.word_index)
        print('Word tokenizer num words:', word_tokenizer.num_words)
        print(word_tokenizer.texts_to_sequences(['asdf efas Huflit']))
        char_tokenizer = Tokenizer(
            filters='\t\n', lower=False, char_level=True, oov_token='<UNK>'
        )
        char_tokenizer.fit_on_texts(re.sub(r'\s', '', line) for line in lines)
        with open('./output/word_tokenizer.pkl', 'wb') as file:
            pickle.dump(word_tokenizer, file, pickle.HIGHEST_PROTOCOL)
        with open('./output/char_tokenizer.pkl', 'wb') as file:
            pickle.dump(char_tokenizer, file, pickle.HIGHEST_PROTOCOL)
