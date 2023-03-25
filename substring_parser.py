from string_to_dataclass import SubstringData, ParsedStringData, ArgumentData


class CHeaderView:
    def __init__(self):
        self.function_type_specifier = ['void',
                                        'char',
                                        'short',
                                        'int',
                                        'long',
                                        'long long',
                                        'float',
                                        'double',
                                        'long double',
                                        'signed',
                                        'unsigned']

        self.lines_to_skip = ['#ifndef', '#include', '#endif']
        self.index = 0
        self.list_length = 0
        self.substring_data = []
        self.parsed_list = []

    def parse_from_string_list(self, substring_data: list[SubstringData]):
        self.substring_data = substring_data
        self.merge_brackets_to_one_line()

        while self.index < self.list_length:
            current_substring = self.substring_data[self.index]
            self.index += 1

            if current_substring.string_value == '' or current_substring.string_value.split()[0] in self.lines_to_skip:
                continue
            if current_substring.string_value.startswith('#define'):
                self.parse_define(current_substring)
                continue
            if current_substring.string_value.startswith('typedef'):
                self.parse_typedef(current_substring)
                continue
            if current_substring.string_value.startswith('struct'):
                self.parse_struct(current_substring)
                continue
            if current_substring.string_value.startswith('inline'):
                # self.parse_inline(current_substring)
                # TODO: бонус1, кому-то надо будет сделать
                continue

            declared_type = current_substring.string_value.split()[0]
            if declared_type in self.function_type_specifier:
                specifier = declared_type
                self.parse_function(current_substring, specifier)
        self.index = 0
        return self.parsed_list

    def merge_brackets_to_one_line(self):
        self.list_length = len(self.substring_data)

        while self.index < self.list_length:
            current_substring = self.substring_data[self.index]

            if '{' not in current_substring.string_value:
                self.index += 1
                continue
            if '}' not in current_substring.string_value:
                self.substring_data[self.index].string_value += self.substring_data[self.index + 1].string_value
                del self.substring_data[self.index + 1]
                self.list_length = len(self.substring_data)
                continue
            self.index += 1
            continue
        self.index = 0

    def parse_typedef(self, data):
        split_typedef = data.string_value.split(' ')

        if split_typedef[1] == 'struct':  # TODO: если структура, то это бонус2. Костя, нужно будет реализовать её
            self.parse_typedef_struct(data)
            return

        typedef = ParsedStringData.parse_function({
            'type': 'typedef',
            'declared_type': str(split_typedef[1]),
            'name': str(split_typedef[2]),
            'line': data.line
        })

        self.function_type_specifier.append(split_typedef[2])
        self.parsed_list.append(typedef)
        
        print(f'Был найден typedef с параметрами: {typedef}')

    def parse_typedef_struct(self, data):
        pass

    def parse_struct(self, data):
        split_struct = data.string_value.split(' ')
        split_fields = split_struct[2:]

        struct = ParsedStringData.parse_function({
            'type': 'struct',
            'name': str(split_struct[1].rstrip(split_struct[1][-1])),
            'args': self.split_fields(split_fields),
            'line': data.line
        })

        self.parsed_list.append(struct)
        print(f'Был найден struct с параметрами: {struct}')



    def parse_define(self, data):
        split_define = data.string_value.split(' ')

        if len(split_define) == 2:  # если например #define HEADER_FILE_H
            return

        if '(' in split_define[1]:  # проверка на аргумент, но я бы улучшил её
            return

        define = ParsedStringData.parse_function({
            'type': 'define',
            'name': str(split_define[1]),
            'value': split_define[2],
            'line': data.line
        })

        self.parsed_list.append(define)
        print(f'Был найден define с параметрами: {define}')

    def parse_function(self, data, return_type):
        split_function = data.string_value.replace('(', ' ').replace(')', ' ').replace(',', ' ')
        split_function = split_function.split()
        name_value = split_function[1]
        del split_function[0:2]
        function = ParsedStringData.parse_function({
            'type': return_type,
            'name': name_value[-1],
            'args': self.split_args(split_function),
            'line': data.line
        })

        self.parsed_list.append(function)
        print(f'Был найден function с параметрами: {function}')

    @staticmethod
    def split_args(split_function: list[str]):
        return_list = []
        while len(split_function) >= 2:
            return_list.append(ArgumentData.from_dict_args(
                {
                    'arg_type': split_function[0],
                    'arg_name': split_function[1]
                }))
            del split_function[0:2]
        return return_list
    
    @staticmethod
    def split_fields(split_struct: list[str]):
        return_list = []
        
        while '' in split_struct:
            split_struct.remove('')
            
        if (len(split_struct) % 2 != 0): # явно что-то не то
            return return_list

        while len(split_struct) >= 2:
            return_list.append(ArgumentData.from_dict_args(
                {
                    'arg_type': split_struct[0],
                    'arg_name': split_struct[1]
                }))
            del split_struct[0:2]

        return return_list

