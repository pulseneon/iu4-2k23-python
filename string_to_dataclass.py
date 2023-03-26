from dataclasses import dataclass
from typing import Optional


@dataclass
class SubstringData:
    string_value: str
    line: int

    @classmethod
    def from_substring(cls, substring: str, line: int):
        return SubstringData(
            substring,
            line
        )


@dataclass
class ArgumentData:
    arg_type: str
    arg_name: str
    arg_exp: str

    @classmethod
    def from_dict_args(cls, arg_details: dict):
        return ArgumentData(
            arg_details['arg_type'],
            arg_details['arg_name'],
            arg_details['arg_exp'] if 'arg_exp' in arg_details else None
        )


@dataclass
class ParsedStringData:
    type: str
    declared_type: str
    name: str
    args: Optional[list[ArgumentData]]
    value: Optional[int]
    line: int

    @classmethod
    def parse_function(cls, string_details: dict):
        return ParsedStringData(
            string_details['type'],
            string_details['declared_type'] if 'declared_type' in string_details else None,
            string_details['name'],
            string_details['args'] if 'args' in string_details else None,
            string_details['value'] if 'value' in string_details else None,
            string_details['line']
        )
