import re
import unicodedata
import string


def clean_text(text):
    text = re.sub("\u2013|\u2014", "-", text)
    text = re.sub("\u00D7", " x ", text)
    text = unicodedata.normalize('NFKC', text)
    for i in string.punctuation:
        text = text.replace(i, ' {} '.format(i))
    text = re.sub(r'[^{}\s\w]+'.format(string.punctuation), ' ', text)
    numbers = re.findall(r'\d+', text)
    text = re.sub(r'\d+', ' 0 ', text)
    # text = re.sub(r'0[ ]*[.,]+[ ]*0', '00', text)
    text = re.sub('[\n\r]+', ' | ', text)
    return re.sub(r'[ ]+', ' ', text), numbers
