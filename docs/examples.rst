Examples
========

Function calls
--------------

Positional arguments:

.. code-block:: python

    your_function(a_param, another_param, a_list, a_dict)

is equivalent to:

.. code-block:: python

    with tracer.start_as_current_span('your_function') as span:
        span.set_attributes({
            'function.call.arg.0.a_param': a_param,
            ...
        })

Named arguments:

.. code-block:: python

    your_function(a_param='a', another_param=2, a_list=[1,2,3], a_dict={'a': 1})

is equivalent to:

.. code-block:: python

    with tracer.start_as_current_span('your_function') as span:
        span.set_attributes({
            'function.call.kwarg.a_param': a_param,
            ...
        })

Span events
-----------

If ``OTELIZE_USE_EVENT_ATTRIBUTES=true``, function arguments and return values are stored as events:

.. code-block:: python

    span.add_event(
        'function.call',
        {
            'args': json.dumps(('a_param', 'another_param')),
            'kwarg': json.dumps({'a_list': [1, 2, 3]}),
            'return_value': None,
        },
    )

Avoid leaks of secrets
----------------------

Set either:

- ``OTELIZE_SPAN_REDACTABLE_ATTRIBUTES`` or
- ``OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX``

to prevent sensitive attributes from being recorded. Redacted attributes will be replaced with ``[REDACTED]``.
