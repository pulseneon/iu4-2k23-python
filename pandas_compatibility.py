import pandas as pd
from main import parse_args, get_file_from_args
from c_header_parser import CHeaderView
import time
import os


def main():
    input_args = parse_args(['', '-f', 'header.h'])

    substring_list = get_file_from_args(input_args.filepath)

    c_parser = CHeaderView()
    c_parser.parse_from_string_list(substring_list)

    df = pd.DataFrame(c_parser.parsed_list, [x.line for x in c_parser.parsed_list])
    df = df.T

    if not os.path.exists('json/'):
        os.mkdir('json/')
    df.to_json(f'json/{time.time()}.json')

    print(df)


if __name__ == '__main__':
    main()
