import json
from typing import Any


class OtelValueConverter:
    DEFAULT_REDACTED_PLACEHOLDER = '[REDACTED]'

    def __init__(self, config, redacted_value=DEFAULT_REDACTED_PLACEHOLDER):
        self.__config = config
        self.__redacted_value = redacted_value

    def to_value(self, value: Any, attr: str | None = None) -> str | int | float | bool:
        if attr and self.__config.span_attribute_is_redactable(attr=attr):
            return self.__redacted_value

        if isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, (list, tuple, set)):
            return json.dumps([self.to_value(v) for v in value])

        if isinstance(value, dict):
            return json.dumps({k: self.to_value(v, attr=k) for k, v in value.items()})

        return str(value)
