import json
import os
import re
from unittest import TestCase
from unittest.mock import MagicMock, patch

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from otelize.decorator import otelize


class TestDecorator(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.span_exporter = InMemorySpanExporter()
        span_processor = SimpleSpanProcessor(self.span_exporter)

        self.tracer_provider = TracerProvider()
        self.tracer_provider.add_span_processor(span_processor)
        self.test_tracer = self.tracer_provider.get_tracer('test')

        tracer_patcher = patch('otelize.decorator.get_otel_tracer')
        self.mock_get_tracer = tracer_patcher.start()
        self.addCleanup(tracer_patcher.stop)
        self.mock_get_tracer.return_value = self.test_tracer

    def tearDown(self) -> None:
        super().tearDown()
        self.span_exporter.clear()
        self.tracer_provider.shutdown()

    @patch('otelize.decorator.Flags')
    def test_decorator_on_args(self, mock_flags_class: MagicMock) -> None:
        mock_flags_class.otelize_include_span_return_value.return_value = True
        mock_flags_class.otelize_span_redactable_attributes.return_value = []
        mock_flags_class.otelize_span_redactable_attribute_regex.return_value = re.compile('token|secret|password')

        @otelize
        def add(a: int, b: int) -> int:
            return a + b

        return_value = add(1, 2)

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestDecorator.test_decorator_on_args.<locals>.add', span.name)
        self.assertEqual(
            {'arg.0.value': 1, 'arg.1.value': 2, 'return.value': return_value},
            dict(span.attributes or {}),
        )

    @patch('otelize.decorator.Flags')
    def test_decorator_on_kwargs(self, mock_flags_class: MagicMock) -> None:
        mock_flags_class.otelize_span_return_value_is_included.return_value = True
        mock_flags_class.otelize_span_redactable_attributes.return_value = []
        mock_flags_class.otelize_span_redactable_attribute_regex.return_value = re.compile('token|secret|password')

        @otelize
        def interpolate(*, string: str, replacements: dict[str, str]) -> str:
            interpolated_string = string
            for name, value in replacements.items():
                placeholder = '{{' + name + '}}'
                interpolated_string = interpolated_string.replace(placeholder, value)
            return interpolated_string

        _string = 'I have to buy three items {{item1}}, {{item2}}, and {{item3}}'
        _replacements = {'item1': 'bread', 'item2': 'milk', 'item3': 'eggs'}
        return_value = interpolate(
            string=_string,
            replacements=_replacements,
        )

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestDecorator.test_decorator_on_kwargs.<locals>.interpolate', span.name)
        self.assertEqual(
            {'string.value': _string, 'replacements.value': json.dumps(_replacements), 'return.value': return_value},
            dict(span.attributes or {}),
        )

    @patch('otelize.decorator.Flags')
    def test_argument_needs_to_be_redacted(self, mock_flags_class: MagicMock) -> None:
        mock_flags_class.otelize_span_return_value_is_included.return_value = True
        mock_flags_class.otelize_span_redactable_attributes.return_value = []
        mock_flags_class.otelize_span_redactable_attribute_regex.return_value = re.compile('token|secret|password')

        @otelize
        def get_token(token_name: str) -> str:
            return os.environ.get(token_name, 'default-token')

        get_token(token_name='my_token')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestDecorator.test_argument_needs_to_be_redacted.<locals>.get_token', span.name)
        self.assertEqual(
            {'token_name.value': '[REDACTED]', 'return.value': 'default-token'},
            dict(span.attributes or {}),
        )

    @patch('otelize.decorator.Flags')
    def test_dict_argument_has_items_that_need_redacting(self, mock_flags_class: MagicMock) -> None:
        mock_flags_class.otelize_span_return_value_is_included.return_value = False
        mock_flags_class.otelize_span_redactable_attributes.return_value = []
        mock_flags_class.otelize_span_redactable_attribute_regex.return_value = re.compile('.*token|secret|password.*')

        @otelize
        def do_something(a_dict: dict[str, str]) -> None:
            pass

        do_something(a_dict={'my_token': 'token', 'my_secret': 'secret', 'a_value': 'value'})

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual(
            'TestDecorator.test_dict_argument_has_items_that_need_redacting.<locals>.do_something', span.name
        )
        self.assertEqual(
            {'a_dict.value': '{"my_token": "[REDACTED]", "my_secret": "secret", "a_value": "value"}'},
            dict(span.attributes or {}),
        )

    @patch('otelize.decorator.Flags')
    def test_return_value_is_not_included(self, mock_flags_class: MagicMock) -> None:
        mock_flags_class.otelize_span_return_value_is_included.return_value = False
        mock_flags_class.otelize_span_redactable_attributes.return_value = []
        mock_flags_class.otelize_span_redactable_attribute_regex.return_value = re.compile('token|secret|password')

        @otelize
        def some_func(param: str) -> str:
            return param

        some_func(param='some_param')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestDecorator.test_return_value_is_not_included.<locals>.some_func', span.name)
        self.assertEqual({'param.value': 'some_param'}, dict(span.attributes or {}))

    def test_use_span(self) -> None:
        @otelize
        def some_func(param: str) -> str:
            func_span = trace.get_current_span()
            func_span.set_attributes({'a_value': 'value', 'another_value': 'another_value'})
            return param

        some_func(param='some_param')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestDecorator.test_use_span.<locals>.some_func', span.name)
        self.assertEqual(
            {'param.value': 'some_param', 'a_value': 'value', 'another_value': 'another_value'},
            dict(span.attributes or {}),
        )
