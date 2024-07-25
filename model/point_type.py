from enum import Enum


class point_type(Enum):
    INTERMEDIATE = "I"
    ENTRY = "E"
    EXIT = "X"
    ARR = "A"
    DEP = "D"

    def __str__(self) -> str:
        return self.value
