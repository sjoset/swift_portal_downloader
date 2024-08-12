from enum import StrEnum, auto


class SwiftDownloadableDataType(StrEnum):
    auxil = auto()
    bat = auto()
    log = auto()
    uvot = auto()
    xrt = auto()

    @classmethod
    def all_data_types(cls):
        return [x for x in cls]
