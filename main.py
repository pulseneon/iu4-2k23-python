import sys
from argparse import ArgumentParser, ArgumentError
from c_header_parser import CHeaderView
from string_to_dataclass import SubstringData


class InputArgumentError(Exception):
    pass


def parse_args(argv):
    try:
        argparser = ArgumentParser(exit_on_error=False)
        argparser.add_argument('-f', '--filepath', type=str, )
        args = argparser.parse_args(argv[1:])
    except ArgumentError as e:
        raise InputArgumentError(f"\nНеверно указан параметр."
                                 f"\nНеправильный параметр: {e.argument_name} "
                                 f"\nОшибка, связанная с ним: {e}")
    return args


def get_file_from_args(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        substring_list = []
        for idx, line in enumerate(f):
            line = line.strip('\n').strip(';')
            substring_list.append(SubstringData.from_substring(line, idx))
        return substring_list


def main(argv):
    substring_list = get_file_from_args(argv.filepath)

    c_parser = CHeaderView()
    c_parser.parse_from_string_list(substring_list)

    print('\n\n')
    for x in c_parser.parsed_list:
        print(x)

    print('\n\n')
    for x in c_parser.substring_data:
        print(x)


if __name__ == '__main__':
    sys_argv = sys.argv
    input_args = parse_args(sys_argv)
    main(input_args)
