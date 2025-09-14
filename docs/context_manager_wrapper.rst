Usage
=====

Introduction
------------

This package provides the ``otelize_context_manager`` wrapper that wraps a context manager,
returning a span and the original result.

Remember that the values are converted to make sure no sensible data is leaked, and that we serialize complex objects.
`View OtelValueConverter <https://github.com/diegojromerolopez/otelize/blob/main/otelize/adapters/otel_value_converter.py>`_.


The otelize context manager wrapper
---------------------

Just wrap otelize_context_manager to your context manager:

.. code-block:: python
    from contextlib import contextmanager
    from otelize import otelize_context_manager

    @contextmanager
    def dummy_cm() -> Generator[str, None, None]:
        yield 'dummy-value'

    with otelize_context_manager(dummy_cm()) as (span, value):
        span.set_attributes({'custom.value': 'my-custom-value'})

The span will contain 'return_value': 'dummy-value' and the 'custom.value': 'my-custom-value'.
