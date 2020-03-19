if __name__ == '__main__':
    import json
    from data_utils.clean_text import clean_text
    from data_utils.constants import ALL_TEXTS
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='./data/train')
    args = parser.parse_args()
    data = [filename for filename in os.listdir(
        args.input) if filename.endswith('.json')]
    with open(os.path.join(os.curdir, ALL_TEXTS), 'w') as file:
        for filename in data:
            with open(os.path.join(args.input, filename), 'r') as in_file:
                in_data = json.load(in_file)
                file.write('\n'.join(clean_text(
                    x['content'])[0] for x in in_data))
