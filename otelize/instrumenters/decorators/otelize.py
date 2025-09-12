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
        return __otelize_function(func=obj)

    if isinstance(obj, type):
        for name, member in vars(obj).items():
            if __instance_method(member, name):
                setattr(obj, name, __otelize_function(func=member, func_type='instance_method'))
            elif __class_method(member):
                func = member.__func__
                setattr(obj, name, classmethod(__otelize_function(func=func, func_type='class_method')))
            elif __static_method(member):
                func = member.__func__
                setattr(obj, name, staticmethod(__otelize_function(func=func, func_type='static_method')))
        return obj

    raise TypeError(f'@otelize not supported on {type(obj)}')


def __instance_method(member, name):
    return isinstance(member, FunctionType) and (not _DUNDER_METHOD_REGEX.match(name))


def __class_method(member):
    return isinstance(member, classmethod)


def __static_method(member):
    return isinstance(member, staticmethod)


def __otelize_function(func: Callable, func_type: _FuncType = 'function') -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = get_otel_tracer()
        with tracer.start_as_current_span(func.__qualname__) as span:
            # If it is a class method (instance, class or static), ignore the implicit parameter
            if func_type.endswith('_method'):
                args_for_span = args[1:]
            else:
                args_for_span = args

            return_value = func(*args, **kwargs)

            span_filler = SpanFiller(
                func_type=func_type,
                span=span,
                func_args=args_for_span,
                func_kwargs=kwargs,
                return_value=return_value,
            )
            span_filler.run()

            return return_value

    return wrapper
