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
        self.original_substring_data = []
        self.parsed_list = []

    def parse_from_string_list(self, substring_data: list[SubstringData]):
        self.original_substring_data = substring_data
        self.merge_brackets_to_one_line()

        while self.index < self.list_length:
            current_substring = self.original_substring_data[self.index]
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
            if current_substring.string_value.startswith('extern'):
                self.parse_extern(current_substring)
                continue
            if current_substring.string_value.startswith('inline'):
                self.parse_inline(current_substring)
                continue

            declared_type = current_substring.string_value.split()[0]
            if declared_type in self.function_type_specifier:
                specifier = declared_type
                self.parse_function(current_substring, specifier)
        self.index = 0
        return self.parsed_list

    def merge_brackets_to_one_line(self):
        self.list_length = len(self.original_substring_data)

        while self.index < self.list_length:
            current_substring = self.original_substring_data[self.index]

            if '{' not in current_substring.string_value:
                self.index += 1
                continue
            if '}' not in current_substring.string_value:
                self.original_substring_data[self.index].string_value += self.original_substring_data[self.index + 1].string_value
                del self.original_substring_data[self.index + 1]
                self.list_length = len(self.original_substring_data)
                continue
            self.index += 1
            continue
        self.index = 0

    def parse_typedef(self, data):
        split_typedef = data.string_value.split()

        if split_typedef[1] == 'struct{':
            self.parse_typedef_struct(data)
            return

        if split_typedef[1] == 'struct':
            split_typedef[1] = split_typedef[3]

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
        split_struct = data.string_value.split()

        split_fields = split_struct[2:]
        split_fields.pop()
        name = split_struct[-1]

        typedef_struct = ParsedStringData.parse_function({
            'type': 'typedef_struct',
            'name': name,
            'args': self.split_fields(split_fields),
            'line': data.line
        })

        self.parsed_list.append(typedef_struct)
        print(f'Был найден typedef_struct с параметрами: {typedef_struct}')

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
        if len(data.string_value.split()) < 5 and '(' not in data.string_value:
            self.parse_global_value(data)
            return

        split_function = data.string_value.replace('(', ' ').replace(')', ' ').replace(',', ' ')
        split_function = split_function.split()
        name_value = split_function[1]
        del split_function[0:2]
        function = ParsedStringData.parse_function({
            'type': return_type,
            'name': name_value,
            'args': self.split_args(split_function),
            'line': data.line
        })

        self.parsed_list.append(function)
        print(f'Был найден function с параметрами: {function}')

    def parse_inline(self, data):
        split_inline = data.string_value.split(' ')

        name_value = split_inline[2].split('(')[0]
        type = split_inline[2].split('(')[1]
        inline = ParsedStringData.parse_function({
            'type': 'inline',
            'declared_type': type,
            'name': name_value,
            'args': self.split_expression(split_inline, self.function_type_specifier),
            'line': data.line
        })

        self.parsed_list.append(inline)
        print(f'Был найден inline с параметрами: {inline}')

    def parse_extern(self, data):
        split_extern = data.string_value.split()
        extern = ParsedStringData.parse_function({
            'type': 'global_value', # жук, я не уверен как его помечать, но скорее всего это просто объявление глобальной переменной
            'declared_type': split_extern[1],
            'name': split_extern[2],
            'line': data.line    
        })

        self.parsed_list.append(extern)
        print(f'Был найден global_value с параметрами: {extern}')

    def parse_global_value(self, data):
        split_value = data.string_value.split()
        global_value = ParsedStringData.parse_function({
            'type': 'global_value',
            'declared_type': split_value[0],
            'name': split_value[1],
            'value': split_value[3],
            'line': data.line
        })

        self.parsed_list.append(global_value)
        print(f'Был найден global_value с параметрами: {global_value}')

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

        while len(split_struct) >= 2:
            return_list.append(ArgumentData.from_dict_args(
                {
                    'arg_type': split_struct[0],
                    'arg_name': split_struct[1].replace('}', '')
                }))
            del split_struct[0:2]

        return return_list
    
    @staticmethod
    def split_expression(split_struct, function_type_specifier):
        return_list = []

        while split_struct:
            if split_struct[0] != '{':
                del split_struct[0]
            else:
                break

        while split_struct:
            declared_type = split_struct[0]
            index = 3
        
            if declared_type and declared_type != '{':
                if declared_type in function_type_specifier:
                    exp = ''
                    while split_struct and split_struct[0]:
                        exp += split_struct.pop(0)
                    return_list.append(ArgumentData.from_dict_args(
                    {
                        'arg_type': declared_type,
                        'arg_name': split_struct[1],
                        'arg_exp': exp
                    }))
                    
                del split_struct[:2]
            else:
                del split_struct[0]

        return return_list
