from opentelemetry import trace


def get_otel_tracer():
    return trace.get_tracer(__name__)
