import tensorflow as tf
import os
from data_utils.constants import SPLIT_TOKEN, TAGS, WORD_TAG_SEPARATOR, CHARACTER_SEPARATOR
import numpy as np


def _split_word2char(words):
    b = tf.string_split(words, CHARACTER_SEPARATOR)
    return tf.string_to_number(tf.sparse_tensor_to_dense(b, default_value='0'))


def _create_iterator(filenames, batch_size, buffer_size, shuffle=False):
    with tf.device('/cpu:0'):
        dataset = tf.data.Dataset.from_tensor_slices(filenames).flat_map(
            lambda filename: tf.data.TextLineDataset(filename).map(
                lambda x: tf.string_split([x], SPLIT_TOKEN).values
            )
        ).cache()
        length = dataset.map(lambda x: tf.squeeze(tf.shape(x))).cache()
        dataset = dataset.map(
            lambda x: tf.transpose(
                tf.reshape(
                    tf.string_split(x, WORD_TAG_SEPARATOR).values,
                    [-1, 4]
                )
            )
        ).cache()
        words = dataset.map(
            lambda x: tf.string_to_number(x[0], tf.int32)
        ).cache()
        characters = dataset.map(
            lambda x: x[1]
        ).map(
            _split_word2char
        ).cache()
        char_length = dataset.map(
            lambda x: tf.string_to_number(x[2], tf.int32)
        ).cache()
        labels = dataset.map(
            lambda x: tf.string_to_number(x[3], tf.int32)
        ).cache()
        words = words.padded_batch(batch_size, [None])
        characters = characters.padded_batch(batch_size, [None, None])
        char_length = char_length.padded_batch(batch_size, [None])
        labels = labels.padded_batch(batch_size, [None], 0)
        length = length.batch(batch_size)
        dataset = tf.data.Dataset.zip(
            (words, length, characters, char_length, labels)
        )
        if shuffle:
            dataset = dataset.shuffle(
                buffer_size=buffer_size,
                reshuffle_each_iteration=True
            )
        iterator = dataset.make_initializable_iterator()
        return iterator


def read_folder(path, batch_size, num_epoch, dev_size, random_seed=None, buffer_size=10000):
    filenames = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                filenames.append(os.path.join(root, file))
    partitions = np.zeros(len(filenames), dtype=np.int32)
    partitions[:int(dev_size*len(filenames)+0.5)] = 1
    if random_seed is not None:
        np.random.seed(random_seed)
    np.random.shuffle(partitions)
    train, test = tf.dynamic_partition(filenames, partitions, 2)
    train_iter = _create_iterator(
        train, batch_size, buffer_size, True
    )
    test_iter = _create_iterator(test, batch_size, buffer_size, False)
    return train_iter, test_iter


if __name__ == '__main__':
    pass
