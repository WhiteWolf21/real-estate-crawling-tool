# coding=utf-8
# sys.path.insert(0, 'D:/BKU/LVTN/CODE/real-estate-chatbot/real-estate-extraction')
import pickle
import numpy as np

from data_utils import constants, get_chunks, transform_data
import tensorflow as tf

class NER(object):
    def __init__(self):
        with open('word_tokenizer.pkl', 'rb') as file:
            self.word_tokenizer = pickle.load(file)
        with open('char_tokenizer.pkl', 'rb') as file:
            self.char_tokenizer = pickle.load(file)

        self.sess = tf.Session()
        meta_graph_def = tf.saved_model.loader.load(
            self.sess,
            [tf.saved_model.tag_constants.SERVING],
            'saved_model'
        )
        signature = meta_graph_def.signature_def
        self.word_ids = self.sess.graph.get_tensor_by_name(
            signature['sequence_tags'].inputs['word_ids'].name)
        self.char_ids = self.sess.graph.get_tensor_by_name(
            signature['sequence_tags'].inputs['char_ids'].name)
        self.sequence_length = self.sess.graph.get_tensor_by_name(
            signature['sequence_tags'].inputs['sequence_length'].name)
        self.word_length = self.sess.graph.get_tensor_by_name(
            signature['sequence_tags'].inputs['word_length'].name)
        self.decode_tags = self.sess.graph.get_tensor_by_name(
            signature['sequence_tags'].outputs['decode_tags'].name)
        self.best_scores = self.sess.graph.get_tensor_by_name(
            signature['sequence_tags'].outputs['best_scores'].name)

    def predict(self, texts):
        transformed = [
            transform_data.transform_data(text, self.word_tokenizer, self.char_tokenizer) for text in texts
        ]
        seq_len = [x[1] for x in transformed]
        words = [x[0] for x in transformed]
        chars = [x[2] for x in transformed]
        word_lengths = transform_data.pad_sequences(
            [x[3] for x in transformed], max(seq_len))
        max_char_len = np.max(word_lengths)
        padded_chars = np.zeros([len(texts), max(seq_len), max_char_len])
        for p1, c1 in zip(padded_chars, chars):
            for i, c2 in enumerate(c1):
                p1[i][:len(c2)] = c2
        feed_dict = {
            self.word_ids: transform_data.pad_sequences(words, max(seq_len)),
            self.sequence_length: seq_len,
            self.char_ids: padded_chars,
            self.word_length: word_lengths
        }
        predicted = self.sess.run([self.decode_tags, self.best_scores], feed_dict=feed_dict)
        origin_words = (x[4] for x in transformed)
        return [
            {
                "tags": [
                    {
                        "content": " ".join(x[0][s:e]),
                        "type":constants.REVERSE_TAGS[t]
                    } for t, s, e in get_chunks.get_chunks(x[1], constants.CLASSES)
                ],
                "score": float(x[2])
            }
            for x in zip(origin_words, predicted[0], predicted[1])
        ]
        return predict


# if __name__ == "__main__":
#     texts = [
#     	"Mua nhà mặt tiền đường Võ Văn Tần tiện kinh doanh",
#         "Mình có nhu cầu mua nhà mặt tiền đường Võ Văn Tần tiện kinh doanh",
#         "Mình cần thuê nhà 1 trệt 1 lầu có phòng ngủ và PK đường Nguyễn Đình Chiểu"
#     ]
#     ner = NER()
#     print(ner.predict(texts))