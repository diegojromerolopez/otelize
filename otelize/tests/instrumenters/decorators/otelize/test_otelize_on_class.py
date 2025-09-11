from otelize.tests.instrumenters.decorators.otelize.base_otelize_test_case import (
    BaseOtelizeTestCase,
)
from otelize.tests.instrumenters.decorators.otelize.dummy_calculator import (
    DummyCalculator,
)


class TestOtelizeOnClass(BaseOtelizeTestCase):
    def test_magic_method(self) -> None:
        calculator = DummyCalculator(initial_value=1)

        str(calculator)

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(0, len(spans))

    def test_instance_method(self) -> None:
        calculator = DummyCalculator(initial_value=1)
        calculator.add(3)
        calculator.subtract(2)

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(2, len(spans))

        span0 = spans[0]
        self.assertEqual('DummyCalculator.add', span0.name)
        self.assertEqual(
            {'function.call.arg.0.value': 3, 'function.call.return.value': 4, 'function.type': 'instance_method'},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('DummyCalculator.subtract', span1.name)
        self.assertEqual(
            {'function.call.arg.0.value': 2, 'function.call.return.value': 2, 'function.type': 'instance_method'},
            dict(span1.attributes or {}),
        )

    def test_static_method(self) -> None:
        DummyCalculator.is_stable()

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(2, len(spans))

        span0 = spans[0]
        self.assertEqual('DummyCalculator._version', span0.name)
        self.assertEqual(
            {'function.call.return.value': '1.2.3', 'function.type': 'static_method'},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('DummyCalculator.is_stable', span1.name)
        self.assertEqual(
            {'function.call.return.value': True, 'function.type': 'static_method'},
            dict(span1.attributes or {}),
        )

    def test_class_method(self) -> None:
        DummyCalculator.set_floating_point_character(',')
        DummyCalculator._uses_comma_float_separator()

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(2, len(spans))

        span0 = spans[0]
        self.assertEqual('DummyCalculator.set_floating_point_character', span0.name)
        self.assertEqual(
            {'function.call.arg.0.value': ',', 'function.call.return.value': 'None', 'function.type': 'class_method'},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('DummyCalculator._uses_comma_float_separator', span1.name)
        self.assertEqual(
            {'function.call.return.value': True, 'function.type': 'class_method'},
            dict(span1.attributes or {}),
        )
