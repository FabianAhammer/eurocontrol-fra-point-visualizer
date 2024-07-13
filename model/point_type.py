from enum import Enum


class PointType(Enum):
    INTERMEDIATE = "green"
    ENTRY = "blue"
    EXIT = "red"
    ARR = "purple"
    DEP = "beige"
    ENTRY_AND_EXIT = "orange"

    def __str__(self):
        return '%s' % self.value
