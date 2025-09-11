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

        tracer_patcher = patch(self._get_otel_tracer_module_path())
        mock_get_tracer = tracer_patcher.start()
        self.addCleanup(tracer_patcher.stop)
        mock_get_tracer.return_value = self.test_tracer

    @staticmethod
    def _get_otel_tracer_module_path() -> str:
        raise NotImplementedError('Implement this method in a subclass')  # pragma: no cover

    def tearDown(self) -> None:
        super().tearDown()
        self.span_exporter.clear()
        self.tracer_provider.shutdown()
