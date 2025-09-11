from collections.abc import Generator

from otelize.instrumenters.wrappers.otelize_iterable import otelize_iterable
from otelize.tests.wrappers.base_otelize_iterable_test_case import (
    BaseOtelizeIterableTestCase,
)


class TestOtelizeOnClass(BaseOtelizeIterableTestCase):
    def test_on_list(self) -> None:
        a_list = ['first', 'second', 'third']
        for span, item in otelize_iterable(a_list):
            span.set_attributes({'item_again': item})

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(3, len(spans))

        span0 = spans[0]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span0.name)
        self.assertEqual(
            {'item.index': 1, 'item.value': 'first', 'item_again': 'first'},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span1.name)
        self.assertEqual(
            {'item.index': 2, 'item.value': 'second', 'item_again': 'second'},
            dict(span1.attributes or {}),
        )

        span2 = spans[2]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span2.name)
        self.assertEqual(
            {'item.index': 3, 'item.value': 'third', 'item_again': 'third'},
            dict(span2.attributes or {}),
        )

    def test_on_set(self) -> None:
        a_set = {'first', 'second', 'third'}
        item_order = []
        for _span, item in otelize_iterable(a_set):
            item_order.append(item)

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(3, len(spans))

        span0 = spans[0]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span0.name)
        self.assertEqual(
            {'item.index': 1, 'item.value': item_order[0]},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span1.name)
        self.assertEqual(
            {'item.index': 2, 'item.value': item_order[1]},
            dict(span1.attributes or {}),
        )

        span2 = spans[2]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span2.name)
        self.assertEqual(
            {'item.index': 3, 'item.value': item_order[2]},
            dict(span2.attributes or {}),
        )

    def test_on_dict(self) -> None:
        a_dict = {'first': 1, 'second': 2, 'third': 3}
        item_order = []
        for _span, item in otelize_iterable(a_dict):
            item_order.append(item)

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(3, len(spans))

        span0 = spans[0]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span0.name)
        self.assertEqual(
            {'item.index': 1, 'item.value': item_order[0]},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span1.name)
        self.assertEqual(
            {'item.index': 2, 'item.value': item_order[1]},
            dict(span1.attributes or {}),
        )

        span2 = spans[2]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span2.name)
        self.assertEqual(
            {'item.index': 3, 'item.value': item_order[2]},
            dict(span2.attributes or {}),
        )

    def test_on_generator(self) -> None:
        def dummy_generator() -> Generator[str, None, None]:
            yield 'first'
            yield 'second'
            yield 'third'

        for _span, _item in otelize_iterable(dummy_generator()):
            pass

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(3, len(spans))

        span0 = spans[0]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span0.name)
        self.assertEqual(
            {'item.index': 1, 'item.value': 'first'},
            dict(span0.attributes or {}),
        )

        span1 = spans[1]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span1.name)
        self.assertEqual(
            {'item.index': 2, 'item.value': 'second'},
            dict(span1.attributes or {}),
        )

        span2 = spans[2]
        self.assertEqual('otelize.instrumenters.wrappers.otelize_iterable', span2.name)
        self.assertEqual(
            {'item.index': 3, 'item.value': 'third'},
            dict(span2.attributes or {}),
        )
