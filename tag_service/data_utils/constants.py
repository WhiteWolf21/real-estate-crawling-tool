from collections import OrderedDict
TAGS = OrderedDict()
TAGS.update([('normal', 'O'),
             ('addr_street', 'STREET'),
             ('addr_district', 'DISTRICT'),
             ('addr_city', 'CITY'),
             ('addr_ward', 'WARD'),
             ('position', 'POSITION'),
             ('area', 'AREA'),
             ('price', 'PRICE'),
             ('transaction_type', 'TRANSACTION_TYPE'),
             ('realestate_type', 'REAL_ESTATE_TYPE'),
             ('legal', 'LEGAL'),
             ('potential', 'POTENTIAL'),
             ('surrounding', 'SURROUNDING_PLACE'),
             ('surrounding_characteristics', 'SURROUNDING_CHARACTERISTIC'),
             ('surrounding_name', 'SURROUNDING_NAME'),
             ('interior_floor', 'FLOOR'),
             ('interior_room', 'ROOM'),
             ('orientation', 'ORIENTATION'),
             ('project', 'PROJECT')])
SPLIT_TOKEN = ' '
B_TOKEN = 'B-{}'
I_TOKEN = 'I-{}'
WORD_TAG_SEPARATOR = '\t'
CHARACTER_SEPARATOR = '|'
ALL_TEXTS = 'all_text.txt'
WORD_VEC_PATH = './output/word_vec.bin'
REVERSE_TAGS = {v: k for k, v in TAGS.items()}

def tags2classes(tags):
    i = 0
    result = {}
    for value in tags:
        if value == TAGS['normal']:
            result[value] = str(i)
            i += 1
        else:
            result[B_TOKEN.format(value)] = str(i)
            result[I_TOKEN.format(value)] = str(i+1)
            i += 2
    return result


CLASSES = tags2classes(TAGS.values())
NUM_CLASSES = len(CLASSES)
if __name__ == '__main__':
    print(CLASSES)
