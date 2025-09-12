from otelize import otelize


@otelize
class DummyCalculator:
    floating_point_character = '.'

    def __init__(self, initial_value: float) -> None:
        self.__value = initial_value

    def __str__(self) -> str:
        return f'Calculator with {self.__value}'

    def add(self, other: float) -> float:
        self.__value += other
        return self.__value

    def subtract(self, other: float) -> float:
        self.__value -= other
        return self.__value

    @classmethod
    def set_floating_point_character(cls, character: str) -> None:
        cls.floating_point_character = character

    @classmethod
    def _uses_comma_float_separator(cls) -> bool:
        return cls.floating_point_character == ','

    @staticmethod
    def is_stable() -> bool:
        version = DummyCalculator._version()
        try:
            return int(version.split('.')[0]) >= 1
        except (IndexError, ValueError):  # pragma: no cover
            return False  # pragma: no cover

    @staticmethod
    def _version() -> str:
        return '1.2.3'
