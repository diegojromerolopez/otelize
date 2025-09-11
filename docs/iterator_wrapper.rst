Usage
=====

Introduction
------------

This package provides the ``otelize_iterable`` wrapper that wraps in a span the yield or looped item,
and returns a span and the item for each loop automatically.

It adds two span attributes automatically for each loop: ``item.index`` and ``item.value``

Remember that the values are converted to make sure no sensible data is leaked, and that we serialize complex objects.
`View OtelValueConverter <https://github.com/diegojromerolopez/otelize/blob/main/otelize/adapters/otel_value_converter.py>`_.


The otelize iterator wrapper
---------------------

Iterables
~~~~~~~~~

Just wrap otelize_iterable to your data structure:

.. code-block:: python
    from otelize import otelize_iterable

    from collections.abc import Generator
    from otelize import otelize_iterable

    my_list = [1, {'a':1}, 'item']

    # For each item it adds {'item.index': index, 'item.value': item}
    # the value is modified according to the OtelValueConverter
    for span, item in otelize_iterable(my_list):
        pass
        # span.set_attributes({ your custom attributes })

Generators
~~~~~~~

The generators can be wrapped in an otelize_iterable and will behave exactly the same than when wrapping iterables:

.. code-block:: python
    from otelize import otelize_iterable

    from collections.abc import Generator
    from otelize import otelize_iterable

    def dummy_generator() -> Generator[str, None, None]:
        yield 'first'
        yield 'second'
        yield 'third'

    # For each yielded item it adds {'item.index': index, 'item.value': item}
    # the value is modified according to the OtelValueConverter
    for span, item in otelize_iterable(dummy_generator()):
        pass
        # span.set_attributes({ your custom attributes })
