Usage
=====

Introduction
------------

This package provides the ``@otelize`` decorator that wraps a function or a class method
in an OTEL span automatically. All arguments of that function will be added as span attributes
(or included in a span event).

Remember that the values are converted to make sure no sensible data is leaked, and that we serialize complex objects.
`View OtelValueConverter <https://github.com/diegojromerolopez/otelize/blob/main/otelize/adapters/otel_value_converter.py>`_.

The otelize decorator
---------------------

Functions
~~~~~~~~~

Just add the decorator to your functions:

.. code-block:: python

    from otelize import otelize

    @otelize
    def your_function(a_param: str, another_param: int, a_list: list[float], a_dict: dict[str, str]):
        ...

All the parameters and the return value will be added as attributes to the OTEL span created
(with an arg or kwarg prefix depending on how it was called).

Classes
~~~~~~~

You can also decorate classes:

.. code-block:: python

    from otelize import otelize

    @otelize
    class DummyCalculator:
        def __init__(self, initial_value: float) -> None:
            self.__value = initial_value

        def add(self, other: float) -> float:
            self.__value += other
            return self.__value

        def subtract(self, other: float) -> float:
            self.__value -= other
            return self.__value

For the non-magic methods of a class, a new span will be created.
This span will contain the arguments used to call the method.
