from otelize.tests.base_otel_test_case import BaseOtelTestCase


class BaseOtelizeIterableTestCase(BaseOtelTestCase):
    @staticmethod
    def _get_otel_tracer_module_path() -> str:
        return 'otelize.instrumenters.wrappers.otelize_iterable.get_otel_tracer'
