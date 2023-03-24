from dataclasses import dataclass


@dataclass
class SubstringData:
    substring: str
    line: int

    @classmethod
    def from_substring(cls, substring: str, line: int):
        return SubstringData(
            substring,
            line
        )
