import json
import os
from unittest.mock import patch

from opentelemetry import trace

from otelize.instrumenters.decorators.otelize import otelize
from otelize.tests.instrumenters.decorators.otelize.base_otelize_test_case import (
    BaseOtelizeTestCase,
)


class TestOtelizeOnFunction(BaseOtelizeTestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_decorator_on_args(self) -> None:
        @otelize
        def add(a: int, b: int) -> int:
            return a + b

        return_value = add(1, 2)

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestOtelizeOnFunction.test_decorator_on_args.<locals>.add', span.name)
        self.assertEqual(
            {
                'function.call.arg.0.value': 1,
                'function.call.arg.1.value': 2,
                'function.call.return.value': return_value,
                'function.type': 'function',
            },
            dict(span.attributes or {}),
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_decorator_on_kwargs(self) -> None:
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
        self.assertEqual('TestOtelizeOnFunction.test_decorator_on_kwargs.<locals>.interpolate', span.name)
        self.assertEqual(
            {
                'function.call.kwarg.string.value': _string,
                'function.call.kwarg.replacements.value': json.dumps(_replacements),
                'function.call.return.value': return_value,
                'function.type': 'function',
            },
            dict(span.attributes or {}),
        )

    @patch.dict(os.environ, {'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX': '.*token|secret.*'}, clear=True)
    def test_argument_needs_to_be_redacted(self) -> None:
        @otelize
        def get_token(token_name: str) -> str:
            return os.environ.get(token_name, 'default-token')

        get_token(token_name='my_token')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestOtelizeOnFunction.test_argument_needs_to_be_redacted.<locals>.get_token', span.name)
        self.assertEqual(
            {
                'function.call.kwarg.token_name.value': '[REDACTED]',
                'function.call.return.value': 'default-token',
                'function.type': 'function',
            },
            dict(span.attributes or {}),
        )

    @patch.dict(os.environ, {'OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX': '.*token|secret.*'}, clear=True)
    def test_dict_argument_has_items_that_need_redacting(self) -> None:
        @otelize
        def do_something(a_dict: dict[str, str]) -> None:
            pass

        do_something(a_dict={'my_token': 'token', 'my_secret': 'secret', 'a_value': 'value'})

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual(
            'TestOtelizeOnFunction.test_dict_argument_has_items_that_need_redacting.<locals>.do_something', span.name
        )
        self.assertEqual(
            {
                'function.call.kwarg.a_dict.value': json.dumps(
                    {'my_token': '[REDACTED]', 'my_secret': 'secret', 'a_value': 'value'},
                ),
                'function.call.return.value': 'None',
                'function.type': 'function',
            },
            dict(span.attributes or {}),
        )

    @patch.dict(os.environ, {'OTELIZE_USE_EVENT_ATTRIBUTES': 'true'}, clear=True)
    def test_add_span_event(self) -> None:
        @otelize
        def some_func(param: str, key_param: str) -> str:
            return param

        some_func('some_param', key_param='some_key_param')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestOtelizeOnFunction.test_add_span_event.<locals>.some_func', span.name)
        self.assertEqual(1, len(span.events))

        span_event = span.events[0]

        self.assertEqual('function.call', span_event.name)
        self.assertEqual(
            {'args': '["some_param"]', 'kwargs': '{"key_param": "some_key_param"}', 'return_value': 'some_param'},
            span_event.attributes,
        )

    @patch.dict(os.environ, {'OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED': 'false'}, clear=True)
    def test_return_value_is_not_included(self) -> None:
        @otelize
        def some_func(param: str) -> str:
            return param

        some_func(param='some_param')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span = spans[0]
        self.assertEqual('TestOtelizeOnFunction.test_return_value_is_not_included.<locals>.some_func', span.name)
        self.assertEqual(
            {
                'function.call.kwarg.param.value': 'some_param',
                'function.type': 'function',
            },
            dict(span.attributes or {}),
        )

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
        self.assertEqual('TestOtelizeOnFunction.test_use_span.<locals>.some_func', span.name)
        self.assertEqual(
            {
                'function.call.kwarg.param.value': 'some_param',
                'a_value': 'value',
                'another_value': 'another_value',
                'function.call.return.value': 'some_param',
                'function.type': 'function',
            },
            dict(span.attributes or {}),
        )
