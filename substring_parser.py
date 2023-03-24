from string_to_dataclass import SubstringData


class CParser:
    def __init__(self):
        self.type_specifier = ['void',
                               'char',
                               'short',
                               'int',
                               '__int8',
                               '__int16',
                               '__int32',
                               '__int64',
                               'long',
                               'long long',
                               'float',
                               'double',
                               'long double',
                               'signed',
                               'unsigned',
                               'struct',
                               'enum',
                               'typedef']

    @staticmethod
    def parse_from_string_list(substring_data: list[SubstringData]):
        index = 0
        list_len = len(substring_data) - 1
        while index <= list_len:
            substring_data[index].index = index
            if '#ifndef' in substring_data[index].substring or '#endif' in substring_data[index].substring:
                del substring_data[index]
                list_len -= 1
                continue
            index += 1
        return substring_data
