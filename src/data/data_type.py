from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class FilterData:
    field: str
    operation: str
    value: str
