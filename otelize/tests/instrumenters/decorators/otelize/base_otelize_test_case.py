from otelize.tests.base_otel_test_case import BaseOtelTestCase


class BaseOtelizeTestCase(BaseOtelTestCase):
    @staticmethod
    def _get_otel_tracer_module_path() -> str:
        return 'otelize.instrumenters.decorators.otelize.get_otel_tracer'
