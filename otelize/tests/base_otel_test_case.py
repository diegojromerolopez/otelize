from unittest import TestCase
from unittest.mock import patch

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


class BaseOtelTestCase(TestCase):
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
