from data_utils.clean_text import clean_text
from data_utils.constants import (B_TOKEN, CHARACTER_SEPARATOR, CLASSES,
                                  I_TOKEN, SPLIT_TOKEN, TAGS,
                                  WORD_TAG_SEPARATOR)


def transform_data(data, word_tokenizer, char_tokenizer):
    """
    Args:
      data (dict): an object with tags attribute that is an object containing (startIdx, value) as (key, value) pair in which
                   value is an object with 3 key: 'type', 'end', 'prev'

    Returns:
      arrays: list of words and corresponding tags.
    """
    words = []
    labels = []
    characters = []
    char_length = []
    text = data['content']
    tags = data['tags']
    for start in sorted(int(x) for x in tags.keys()):
        tag = tags[str(start)]
        end = tag['end']
        _type = tag['type']
        tokens, _ = clean_text(text[start:end])
        words.extend(
            str(x) for x in word_tokenizer.texts_to_sequences([tokens])[0]
        )
        tokens = tokens.split()
        characters.extend(
            CHARACTER_SEPARATOR.join(str(x) for x in char_tokenizer.texts_to_sequences([x.strip()])[0]) for x in tokens
        )
        char_length.extend(str(len(x.strip())) for x in tokens)
        if _type == 'normal':
            labels.extend(CLASSES[TAGS[_type]] for _ in tokens)
        else:
            labels.extend(
                CLASSES[B_TOKEN.format(TAGS[_type])] if i == 0 else CLASSES[I_TOKEN.format(TAGS[_type])] for i, _ in enumerate(tokens)
            )
    return words, characters, char_length, labels


if __name__ == '__main__':
    import json
    import pickle
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--word_tokenizer', type=str,
                        default='./output/word_tokenizer.pkl')
    parser.add_argument('--char_tokenizer', type=str,
                        default='./output/char_tokenizer.pkl')
    parser.add_argument('--output', type=str, default='./output/data')
    parser.add_argument('--input', type=str, default='./data/train')
    args = parser.parse_args()
    with open(args.word_tokenizer, 'rb') as file:
        word_tokenizer = pickle.load(file)
    with open(args.char_tokenizer, 'rb') as file:
        char_tokenizer = pickle.load(file)
    data = [filename for filename in os.listdir(
        args.input) if filename.endswith('.json')]
    class_count = {}
    for filename in data:
        with open(os.path.join(args.input, filename), 'r') as file:
            data = json.load(file)
            # print(char_tokenizer.word_index)
            # print(word_tokenizer.word_index)
            for i, v in enumerate(data):
                if 'tags' not in v:
                    continue
                for tag in v['tags'].values():
                    tag = tag['type']
                    if class_count.get(tag):
                        class_count[tag]['count'] += 1
                    else:
                        class_count[tag] = {'count': 1}
                path = os.path.join(args.output, filename.split('.')[0])
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(os.path.join(path, '{}.txt'.format(i)), 'w') as file:
                    a, b, c, d = transform_data(
                        v, word_tokenizer, char_tokenizer
                    )
                    file.write(SPLIT_TOKEN.join('\t'.join(token)
                                                for token in zip(a, b, c, d)))
    import pandas as pd
    final_counts = pd.DataFrame.from_dict(class_count, 'index')
    final_counts.to_csv('output/class_count.csv')
    print(final_counts)
