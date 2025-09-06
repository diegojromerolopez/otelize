import json
import os
import re
from json import JSONDecodeError


class Config:
    OTELIZE_USE_SPAN_ATTRIBUTES = 'OTELIZE_USE_SPAN_ATTRIBUTES'
    OTELIZE_USE_EVENT_ATTRIBUTES = 'OTELIZE_USE_EVENT_ATTRIBUTES'
    OTELIZE_SPAN_REDACTABLE_ATTRIBUTES = 'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES'
    OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX = 'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX'
    OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED = 'OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED'

    NOTHING = r'(?!)'

    def __init__(self) -> None:
        self.__use_span_attributes: bool = False
        self.__use_event_attributes: bool = False
        self.__span_redactable_attributes: list[str] = []
        self.__span_redactable_attribute_regex: re.Pattern[str] = re.compile(self.NOTHING)
        self.__span_return_value_is_included: bool = False
        self.__load()

    def __load(self):
        self.__use_span_attributes = self.__otelize_use_span_attributes()
        self.__use_event_attributes = self.__otelize_use_event_attributes()
        self.__span_redactable_attributes = self.__otelize_span_redactable_attributes()
        self.__span_redactable_attribute_regex = self.__otelize_span_redactable_attribute_regex()
        self.__span_return_value_is_included = self.__otelize_span_return_value_is_included()

    @staticmethod
    def get() -> 'Config':
        global _CONFIG
        _CONFIG = Config()
        return _CONFIG

    @property
    def use_span_attributes(self) -> bool:
        return self.__use_span_attributes

    @property
    def use_event_attributes(self) -> bool:
        return self.__use_event_attributes

    def span_attribute_is_redactable(self, attr: str) -> bool:
        if attr in self.__span_redactable_attributes:
            return True
        if self.__span_redactable_attribute_regex.match(attr):
            return True
        return False

    @property
    def span_return_value_is_included(self) -> bool:
        return self.__span_return_value_is_included

    def __otelize_use_span_attributes(self) -> bool:
        return bool(os.environ.get(self.OTELIZE_USE_SPAN_ATTRIBUTES, 'true').lower() == 'true')

    def __otelize_use_event_attributes(self) -> bool:
        return bool(os.environ.get(self.OTELIZE_USE_EVENT_ATTRIBUTES, 'false').lower() == 'true')

    def __otelize_span_redactable_attributes(self) -> list[str]:
        try:
            return json.loads(os.environ.get(self.OTELIZE_SPAN_REDACTABLE_ATTRIBUTES, '[]'))
        except JSONDecodeError:
            return []

    def __otelize_span_redactable_attribute_regex(self) -> re.Pattern[str]:
        try:
            return re.compile(str(os.environ.get(self.OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX, self.NOTHING)))
        except re.error:
            return re.compile(self.NOTHING)

    def __otelize_span_return_value_is_included(self) -> bool:
        return bool(os.environ.get(self.OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED, 'true').lower() == 'true')


_CONFIG: Config | None = None
