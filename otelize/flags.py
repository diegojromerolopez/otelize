import json
import os
import re
from json import JSONDecodeError


class Flags:
    NOTHING = r'(?!)'

    @staticmethod
    def otelize_span_redactable_attributes() -> list[str]:
        try:
            return json.loads(os.environ.get('OTELIZE_SPAN_REDACTABLE_ATTRIBUTES', '[]'))
        except JSONDecodeError:
            return []

    @classmethod
    def otelize_span_redactable_attribute_regex(cls) -> re.Pattern[str]:
        try:
            return re.compile(str(os.environ.get('OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX', cls.NOTHING)))
        except re.error:
            return re.compile(cls.NOTHING)

    @staticmethod
    def otelize_span_return_value_is_included() -> bool:
        return bool(os.environ.get('OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED', False))
