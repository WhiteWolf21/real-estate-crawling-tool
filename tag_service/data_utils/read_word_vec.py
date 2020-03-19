import fastText
import numpy as np
import pickle


def read_word_vec(path, word_tokenizer):
    model = fastText.load_model(path)
    word_index = word_tokenizer.word_index
    embedding = np.zeros([len(word_index)+1, model.get_dimension()])
    for v, i in word_index.items():
        embedding[i] = model.get_word_vector(v)
    return embedding


def read_polyglot(path, word_tokenizer):
    with open(path, 'rb') as file:
        model = pickle.load(file, encoding='bytes')
    word_index = word_tokenizer.word_index
    embedding = np.zeros([len(word_index)+1, len(list(model.values())[0])])
    for v, i in word_index.items():
        if v in model:
            embedding[i] = model[v]
    return embedding


if __name__ == '__main__':
    from data_utils.constants import WORD_VEC_PATH
    import pickle
    with open('output/word_tokenizer.pkl', 'rb') as file:
        word_tokenizer = pickle.load(file)
    print(word_tokenizer.word_index[word_tokenizer.oov_token])
    print(len(word_tokenizer.word_index))
    model = fastText.load_model(WORD_VEC_PATH)
    embedding = read_word_vec(WORD_VEC_PATH, word_tokenizer)
    assert(np.sum(embedding[word_tokenizer.word_index['nhà']]
                  == model.get_word_vector('nhà')) == model.get_dimension())
    assert(np.sum(embedding[word_tokenizer.word_index['Bán']]
                  == model.get_word_vector('Bán')) == model.get_dimension())
    assert(np.sum(embedding[word_tokenizer.word_index['tầng']]
                  == model.get_word_vector('tầng')) == model.get_dimension())
    assert(np.sum(embedding[word_tokenizer.word_index['<UNK>']]
                  == model.get_word_vector('<UNK>')) == model.get_dimension())
    print(embedding[word_tokenizer.word_index[word_tokenizer.oov_token]])
