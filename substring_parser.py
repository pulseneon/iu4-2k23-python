from string_to_dataclass import SubstringData


class CParser:
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
        
        self.parsed_list = []

    def parse_from_string_list(self, substring_data: list[SubstringData]):
        for data in substring_data:
            if data.substring.startswith('#define'):
                self.parse_define(data)
            elif data.substring.startswith('typedef'):
                self.parse_typedef(data)
            for specifier in self.function_type_specifier:
                if data.substring.startswith(specifier):
                    self.parse_function(data, specifier)
                    break

    def parse_typedef(self, data):
        split_typedef = data.substring.split(' ')

        if split_typedef[1] == 'struct': # исключение если это структура
            return

        typedef = {
            'type':'typedef',
            'target_type': str(split_typedef[1]),
            'declared_type': str(split_typedef[2]),
            'index': data.index
            }
        
        self.parsed_list.append(typedef)
        print(f'Был найден typedef с параметрами: {typedef}')

    def parse_define(self, data):
        split_define = data.substring.split(' ')

        if len(split_define) < 3: # если например #define HEADER_FILE_H
            return
        
        if '(' in split_define[1]: # проверка на аргумент, но я бы улучшил её
            return 
        
        define = {
            'type':'define',
            'name': str(split_define[1]),
            'value': split_define[2],
            'index': data.index
        }

        self.parsed_list.append(define)
        print(f'Был найден define с параметрами: {define}')

    def parse_function(self, data, return_type):
        split_function = data.substring.split(' ')

        function = {
            'type': 'function',
            'return': split_function[0],
            'name': split_function[1],
            'args':[
                # нужно разобрать их в скобочках как-то аккуратно
            ],
            'index': data.index
        }

        self.parsed_list.append(function)
        print(f'Был найден function с параметрами: {function}')