from collections.abc import Generator, Iterable
from typing import TypeVar

from opentelemetry.trace import Span

from otelize.adapters.otel_value_converter import OtelValueConverter
from otelize.infra.config import Config
from otelize.infra.tracer import get_otel_tracer

T = TypeVar('T')


def otelize_iterable(
    items: Iterable[T],
    span_name: str = __name__,
) -> Generator[tuple[Span, T], None, None]:
    tracer = get_otel_tracer()

    otel_value_converter = OtelValueConverter(config=Config.get())

    # create span once when generator starts
    for index, item in enumerate(items, start=1):
        with tracer.start_as_current_span(span_name) as span:
            span.set_attributes({'item.index': index, 'item.value': otel_value_converter.to_value(value=item)})
            yield span, item
