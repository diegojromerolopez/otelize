import os
from unittest import TestCase
from unittest.mock import patch

from otelize.infra.config import Config


class TestConfig(TestCase):
    def test_use_span_attributes_not_set(self) -> None:
        self.assertTrue(Config.get().use_span_attributes)

    @patch.dict(os.environ, {'OTELIZE_USE_SPAN_ATTRIBUTES': 'true'}, clear=True)
    def test_use_span_attributes_set_to_true(self) -> None:
        self.assertTrue(Config.get().use_span_attributes)

    @patch.dict(os.environ, {'OTELIZE_USE_SPAN_ATTRIBUTES': 'false'}, clear=True)
    def test_use_span_attributes_set_to_false(self) -> None:
        self.assertFalse(Config.get().use_span_attributes)

    def test_use_event_attributes_not_set(self) -> None:
        self.assertFalse(Config.get().use_event_attributes)

    @patch.dict(os.environ, {'OTELIZE_USE_EVENT_ATTRIBUTES': 'true'}, clear=True)
    def test_use_event_attributes_set_to_true(self) -> None:
        self.assertTrue(Config.get().use_event_attributes)

    @patch.dict(os.environ, {'OTELIZE_USE_EVENT_ATTRIBUTES': 'false'}, clear=True)
    def test_use_event_attributes_set_to_false(self) -> None:
        self.assertFalse(Config.get().use_event_attributes)

    def test_span_redactable_attributes_not_set(self) -> None:
        self.assertFalse(Config.get().span_attribute_is_redactable('an_attribute'))

    @patch.dict(os.environ, {'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES': '["my-secret"]'}, clear=True)
    def test_span_redactable_attributes_set_and_attribute_in_list(self) -> None:
        self.assertTrue(Config.get().span_attribute_is_redactable('my-secret'))

    @patch.dict(os.environ, {'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES': '["my-secret"]'}, clear=True)
    def test_span_redactable_attributes_set_and_attribute_not_in_list(self) -> None:
        self.assertFalse(Config.get().span_attribute_is_redactable('not-a-secret'))

    @patch.dict(os.environ, {'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX': '.*secret|token.*'}, clear=True)
    def test_span_redactable_attributes_regex_set_and_attribute_match(self) -> None:
        self.assertTrue(Config.get().span_attribute_is_redactable('my-secret'))

    @patch.dict(os.environ, {'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX': '.*secret|token.*'}, clear=True)
    def test_span_redactable_attributes_regex_set_and_attribute_not_match(self) -> None:
        self.assertFalse(Config.get().span_attribute_is_redactable('an_attribute'))

    def test_span_return_value_is_included_not_set(self) -> None:
        self.assertTrue(Config.get().span_return_value_is_included)

    @patch.dict(os.environ, {'OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED': 'true'}, clear=True)
    def test_span_return_value_is_included_set_to_true(self) -> None:
        self.assertTrue(Config.get().span_return_value_is_included)

    @patch.dict(os.environ, {'OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED': 'false'}, clear=True)
    def test_span_return_value_is_included_set_to_false(self) -> None:
        self.assertFalse(Config.get().span_return_value_is_included)
