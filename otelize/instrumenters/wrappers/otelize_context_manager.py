from contextlib import contextmanager
from typing import ContextManager, Iterator, TypeVar

from opentelemetry.trace import Span

from otelize.adapters.otel_value_converter import OtelValueConverter
from otelize.infra.config import Config
from otelize.infra.tracer import get_otel_tracer

T = TypeVar('T')


@contextmanager
def otelize_context_manager(
    context_manager: ContextManager[T],
    span_name: str = __name__,
) -> Iterator[tuple[Span, T]]:
    tracer = get_otel_tracer()
    otel_value_converter = OtelValueConverter(config=Config.get())
    with tracer.start_as_current_span(span_name) as span:
        with context_manager as return_value:
            span.set_attributes({'return_value': otel_value_converter.to_value(value=return_value)})
            yield span, return_value
