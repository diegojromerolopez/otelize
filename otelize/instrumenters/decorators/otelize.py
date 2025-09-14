import re
from collections.abc import Callable
from functools import wraps
from types import FunctionType
from typing import Literal

from otelize.infra.tracer import get_otel_tracer
from otelize.instrumenters.decorators.span_filler import SpanFiller

_DUNDER_METHOD_REGEX = re.compile(r'^__\w+__$')

_FuncType = Literal['function', 'instance_method', 'static_method', 'class_method']


def otelize(obj):
    if isinstance(obj, FunctionType):
        return __otelize_function(func=obj, func_type=__func_type(obj))

    if isinstance(obj, type):
        for name, member in vars(obj).items():
            if _DUNDER_METHOD_REGEX.match(name):
                continue
            elif isinstance(member, FunctionType):
                setattr(obj, name, otelize(member))
            elif isinstance(member, classmethod):
                setattr(obj, name, otelize(member))
            elif isinstance(member, staticmethod):
                setattr(obj, name, otelize(member))
        return obj

    if isinstance(obj, classmethod):
        func = obj.__func__
        return classmethod(__otelize_function(func=func, func_type='class_method'))

    if isinstance(obj, staticmethod):
        func = obj.__func__
        return staticmethod(__otelize_function(func=func, func_type='static_method'))

    raise TypeError(f'@otelize not supported on {type(obj)}')


def __func_type(func: Callable) -> _FuncType:
    if 'self' in func.__code__.co_varnames:
        return 'instance_method'
    if isinstance(func, classmethod):
        return 'class_method'
    if isinstance(func, staticmethod):
        return 'static_method'
    return 'function'


def __otelize_function(func: Callable, func_type: _FuncType = 'function') -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = get_otel_tracer()
        with tracer.start_as_current_span(func.__qualname__) as span:
            func_parameters = func.__code__.co_varnames
            # If it is a class method (instance, class or static), ignore the implicit parameter
            if func_type in {'class_method', 'static_method', 'instance_method'}:
                args_for_span = args[1:]
                func_parameters = func_parameters[1:]
            else:
                args_for_span = args

            return_value = func(*args, **kwargs)

            span_filler = SpanFiller(
                func_type=func_type,
                span=span,
                parameters=func_parameters,
                func_args=args_for_span,
                func_kwargs=kwargs,
                return_value=return_value,
            )
            span_filler.run()

            return return_value

    return wrapper
