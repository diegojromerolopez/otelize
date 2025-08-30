import json
import re
from functools import wraps
from typing import Any

from opentelemetry.trace import Span

from otelize.flags import Flags
from otelize.tracer import get_otel_tracer

_REDACTABLE_ARGUMENT_REGEX = re.compile('.*(token|secret|password).*', re.IGNORECASE)


def otelize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = get_otel_tracer()
        with tracer.start_as_current_span(func.__qualname__) as span:
            __set_args_to_span_attributes(func_args=args, span=span)
            __set_kwargs_to_span_attributes(func_kwargs=kwargs, span=span)
            return_value = func(*args, **kwargs)
            __set_return_value_to_span_attributes(return_value=return_value, span=span)
            return return_value

    return wrapper


def __set_args_to_span_attributes(func_args: tuple[Any, ...], span: Span) -> None:
    for arg_index, arg in enumerate(func_args):
        attr_name = f'arg.{arg_index}.value'
        span.set_attribute(attr_name, __value_as_span_attribute(attr=attr_name, value=arg))


def __set_kwargs_to_span_attributes(func_kwargs: dict[str, Any], span: Span) -> None:
    for key, value in func_kwargs.items():
        span.set_attribute(f'{key}.value', __value_as_span_attribute(attr=key, value=value))


def __value_as_span_attribute(attr: str, value: Any) -> str | int | float | bool:
    if attr in Flags.otelize_span_redactable_attributes() or Flags.otelize_span_redactable_attribute_regex().match(
        attr
    ):
        return '[REDACTED]'

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, (list, tuple, set)):
        return json.dumps(value)

    if isinstance(value, dict):
        redacted_dict = {k: __value_as_span_attribute(attr=k, value=v) for k, v in value.items()}
        return json.dumps(redacted_dict)

    return str(value)


def __set_return_value_to_span_attributes(return_value: Any, span: Span) -> None:
    if not Flags.otelize_span_return_value_is_included():
        return
    span.set_attribute('return.value', __value_as_span_attribute(attr='return_value', value=return_value))
