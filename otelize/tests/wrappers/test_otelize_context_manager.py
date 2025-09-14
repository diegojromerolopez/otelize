import tempfile
from collections.abc import Generator
from contextlib import contextmanager

from otelize.instrumenters.wrappers.otelize_context_manager import (
    otelize_context_manager,
)
from otelize.tests.base_otel_test_case import BaseOtelTestCase


class TestOtelizeContextManager(BaseOtelTestCase):
    @staticmethod
    def _get_otel_tracer_module_path() -> str:
        return 'otelize.instrumenters.wrappers.otelize_context_manager.get_otel_tracer'

    def test_otelize_open_file_context_manager(self) -> None:
        with otelize_context_manager(tempfile.NamedTemporaryFile()) as (span, temp_file):
            temp_file.write(b'hello')

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span0 = spans[0]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_context_manager', span0.name)
        self.assertEqual(
            {'return_value': temp_file.name},
            dict(span0.attributes or {}),
        )

    def test_otelize_custom_context_manager(self) -> None:
        @contextmanager
        def dummy_context() -> Generator[str, None, None]:
            yield 'dummy-value'

        with otelize_context_manager(dummy_context()) as (span, value):
            span.set_attributes({'custom.value': 'my-custom-value'})

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(1, len(spans))

        span0 = spans[0]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_context_manager', span0.name)
        self.assertEqual(
            {'return_value': 'dummy-value', 'custom.value': 'my-custom-value'},
            dict(span0.attributes or {}),
        )
