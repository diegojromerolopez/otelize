Usage
=====

Introduction
------------

``otelize`` is a simple package for developers that want to add basic
OpenTelemetry (OTEL) telemetry to their projects without adding much boilerplate.

How it works
------------

This package provides the ``@otelize`` decorator that wraps a function or a class method
in an OTEL span automatically. All arguments of that function will be added as span attributes
(or included in a span event).

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

All the parameters and the return value will be added as attributes to the OTEL span created.

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
