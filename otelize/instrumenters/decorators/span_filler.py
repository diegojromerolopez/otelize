from typing import Any, Literal

from opentelemetry.trace import Span

from otelize.adapters.otel_value_converter import OtelValueConverter
from otelize.infra.config import Config

_FuncType = Literal['function', 'instance_method', 'static_method', 'class_method']


class SpanFiller:
    def __init__(
        self,
        func_type: _FuncType,
        span: Span,
        func_args: tuple[Any, ...],
        func_kwargs: dict[str, Any],
        return_value: Any,
    ) -> None:
        self.__func_type = func_type
        self.__config = Config.get()
        self.__span = span
        self.__func_args = func_args
        self.__func_kwargs = func_kwargs
        self.__return_value = return_value
        self.__otel_value_converter = OtelValueConverter(config=self.__config)

    def run(self) -> None:
        if self.__config.use_span_attributes:
            self.__assign_span_attrs()
        if self.__config.use_event_attributes:
            self.__create_span_event()

    def __assign_span_attrs(self) -> None:
        self.__span.set_attributes({'function.type': self.__func_type})

        for arg_index, arg in enumerate(self.__func_args):
            attr_name = f'function.call.arg.{arg_index}.value'
            self.__span.set_attribute(attr_name, self.__otel_value_converter.to_value(value=arg))

        for key, value in self.__func_kwargs.items():
            self.__span.set_attribute(
                f'function.call.kwarg.{key}.value', self.__otel_value_converter.to_value(attr=key, value=value)
            )

        if self.__config.span_return_value_is_included:
            self.__span.set_attribute(
                'function.call.return.value', self.__otel_value_converter.to_value(value=self.__return_value)
            )

    def __create_span_event(self) -> None:
        self.__span.add_event(
            'function.call',
            {
                'args': self.__otel_value_converter.to_value(value=self.__func_args),
                'kwargs': self.__otel_value_converter.to_value(value=self.__func_kwargs),
                'return_value': self.__otel_value_converter.to_value(value=self.__return_value),
            },
        )
