Advanced usage
==============

Adding additional information
-----------------------------

Inside a decorated function, you can access the current span, and add your own attributes:

.. code-block:: python

    from opentelemetry import trace
    from otelize import otelize

    @otelize
    def your_function(a_param: str, another_param: int, and_another_one: Any):
        span = trace.get_current_span()
        span.set_attribute('custom_attr', 'your value')
