from dataclasses import dataclass


@dataclass
class SubstringData:
    substring: str
    index: int

    @classmethod
    def from_substring(cls, substring: str, index: int):
        return SubstringData(
            substring,
            index
        )
