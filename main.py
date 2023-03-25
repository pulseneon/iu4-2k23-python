import sys
from argparse import ArgumentParser, ArgumentError
from substring_parser import CParser
from string_to_dataclass import SubstringData
header_parser = CParser()


class InputArgumentError(Exception):
    pass


def parse_args(argv):
    try:
        argparser = ArgumentParser(exit_on_error=False)
        argparser.add_argument('-f', '--filepath', type=str)
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
            substring_list.append(SubstringData.from_substring(line, idx))
        return substring_list


def main(argv):
    substring_list = get_file_from_args(argv.filepath)
    parsed_substrings = header_parser.parse_from_string_list(substring_list)

    parser = CParser()
    parser.parse_from_string_list(parsed_substrings)


if __name__ == '__main__':
    input_arguments = parse_args(sys.argv)
    main(input_arguments)
