# otelize

![test](https://github.com/diegojromerolopez/otelize/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/otelize/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/otelize.svg)](https://pypi.python.org/pypi/otelize/)
[![PyPI version otelize](https://badge.fury.io/py/otelize.svg)](https://pypi.python.org/pypi/otelize/)
[![PyPI status](https://img.shields.io/pypi/status/otelize.svg)](https://pypi.python.org/pypi/otelize/)
[![PyPI download month](https://img.shields.io/pypi/dm/otelize.svg)](https://pypi.python.org/pypi/otelize/)

Add OTEL auto-instrumentation to your functions.

## Introduction
This is a simple package intended for the use of lazy developers that want to included basic OTEL telemetry to their
project without bothering much with adding a lot of boilerplate. 

## How it works
This package provides the otelize decorator that wraps a function and adds all your parameters (with their values) and
the returning value as span attributes. 

## How to use it

See the [official documentation in readthedocs.io](https://otelize.readthedocs.io/en/latest/).

### The otelize decorator

This package provides an `@otelize` decorator for applying it on functions and classes.

#### The otelize decorator on functions

Just add the `@otelize` decorator to your functions:

```python
from otelize import otelize

@otelize
def your_function(a_param: str, another_param: int, a_list: list[float], a_dict: dict[str, str]):
    ...
```

All the parameters and the return value will be added as attributes to the OTEL span created for the function.

In this case, and if you call the arguments as positional arguments, e.g.

```python
your_function(a_param, another_param, a_list, a_dict)
```

it would be equivalent to doing:

```python
import json

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def your_function(a_param: str, another_param: int, a_list: list[float], a_dict: dict[str, str]):
    with tracer.start_as_current_span('your_function') as span:
        span.set_attributes({
            'function.call.arg.0.a_param': a_param,
            'function.call.arg.1.another_param': another_param,
            'function.call.arg.1.a_list': json.dumps(a_list),
            'function.call.arg.1.a_dict': json.dumps(a_dict),
        })
```

On the other hand, in the case of using named-arguments, it will be slightly different, e.g.

```python
your_function(a_param='a', another_param=2, a_list=[1,2,3], a_dict={'a': 1})
```

it would be equivalent to doing:

```python
import json

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def your_function(a_param: str, another_param: int, a_list: list[float], a_dict: dict[str, str]):
    with tracer.start_as_current_span('your_function') as span:
        span.set_attributes({
            'function.call.kwarg.a_param': a_param,
            'function.call.kwarg.another_param': another_param,
            'function.call.kwarg.a_list': json.dumps(a_list),
            'function.call.kwarg.a_dict': json.dumps(a_dict),
        })
```

#### The otelize decorator on classes

Just add the @otelize decorator to a class, like in the following example:

```python
from otelize import otelize

@otelize
class DummyCalculator:
    floating_point_character = '.'

    def __init__(self, initial_value: float) -> None:
        self.__value = initial_value

    def __str__(self) -> str:
        return f'Calculator with {self.__value}'

    def add(self, other: float) -> float:
        self.__value += other
        return self.__value

    def subtract(self, other: float) -> float:
        self.__value -= other
        return self.__value
```

This will add a span context in each instance method, class method or static method.

The arguments will be added in the same way that they were being added to functions.

There is a limitation, that is that the dunder methods (e.g. `__method__`) are ignored.

### The otelize_iterable wrapper

#### otelize_iterable on iterables

Just wrap your loopable data structure with the otelize_iterable wrapper to get a generator that yields a span
and the item.

```python
from otelize import otelize_iterable

for span, item in otelize_iterable([1, 2, 3]):
    pass
    # span.set_attributes({ your other attributes })
```

#### otelize_iterable on generators

Just wrap your iterable with the otelize_iterable wrapper to get a generator that yields a span and the item.

```python
from collections.abc import Generator
from otelize import otelize_iterable


def dummy_generator() -> Generator[str, None, None]:
    yield 'first'
    yield 'second'
    yield 'third'


for span, item in otelize_iterable(dummy_generator()):
    pass
    # span.set_attributes({ your other attributes })
```

### Configuration

The following configuration settings can be set via environment variables:

- `OTELIZE_USE_SPAN_ATTRIBUTES`: if true it will use OTEL span attributes. By default is `'true'`.
- `OTELIZE_USE_EVENT_ATTRIBUTES`: if true it will create anew OTEL event with attributes. By default is `'true'`.
- `OTELIZE_SPAN_REDACTABLE_ATTRIBUTES`: JSON array of attributes that need to be redacted in your OTEL. By default is `'[]'`
- `OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX`: string with a Python regex that will redact all attributes that match the regulax expression. By default, is an impossible regex: `'(?!)'`.
- `OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED`: Truthy or falsy value. By default, it is `'true'`.

### Use span events

If you set the environment variable `OTELIZE_USE_EVENT_ATTRIBUTES` to true, a new span event will be added with the
function arguments and return value.

For example:

This call

```python

your_function('a_param', 'another_param', a_list=[1, 2, 3], a_dict={'a': 'a'})

```

would be equal to this code:

```python
import json

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def your_function(a_param: str, another_param: int, a_list: list[float], a_dict: dict[str, str]):
    with tracer.start_as_current_span('your_function') as span:
        span.add_event(
            'function.call', {
                'args': json.dumps(('a_param', 'another_param')),
                'kwarg': json.dumps({'a_list': [1, 2, 3], 'a_dict': {'a': 'a'}}),
                'return_value': None,
            },
        )
```

### Avoid leaks of secrets

To avoid leaking values of sensitive parameters, define the following environment values:

- `OTELIZE_SPAN_REDACTABLE_ATTRIBUTES` or
- `OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX`

The redacted attributes will have the `'[REDACTED]'` value.

### Adding additional information from the decorated function

Call `trace.get_current_span()` to get the current span from inside the function:

```python
from typing import Any
from opentelemetry import trace
from otelize import otelize


@otelize
def your_function(a_param: str, another_param: int, and_another_one: Any):
    span = trace.get_current_span()
    span.set_attribute('custom_attr', 'your value')
```

### Examples
There are more examples in the [test folder](otelize/tests).

## Dependencies
The runtime depends only on [opentelemetry-api](https://pypi.org/project/opentelemetry-api/), and for testing
it depends on [opentelemetry-sdk](https://pypi.org/project/opentelemetry-sdk/) and other test coverage and
formatting packages (coverage, black, flake8...).

## Python version support
The minimum Python supported version is 3.10.

## Collaborations
This project is open to collaborations. Make a PR or an issue,
and I'll take a look to it.

## License
[MIT](LICENSE) license, but if you need any other contact me.

## Disclaimer
This project is not affiliated with, endorsed by, or sponsored by
the [OpenTelemetry](https://opentelemetry.io/) project owners,
the [Cloud Native Computing Foundation](https://www.cncf.io/).

The use of the names "OTEL" and "otelize"
in this repository is solely for descriptive purposes
and does not imply any association or intent to infringe
on any trademarks.

The project is named "otelize" for purposes of having
a short name that can be used as a Python decorator.
