Configuration
=============

The following settings can be set via environment variables:

- ``OTELIZE_USE_SPAN_ATTRIBUTES``: if true it will use OTEL span attributes. Default: ``true``.
- ``OTELIZE_USE_EVENT_ATTRIBUTES``: if true it will create a new OTEL event with attributes. Default: ``true``.
- ``OTELIZE_SPAN_REDACTABLE_ATTRIBUTES``: JSON array of attributes to be redacted. Default: ``[]``.
- ``OTELIZE_SPAN_REDACTABLE_ATTRIBUTES_REGEX``: regex for redacting attributes. Default: ``(?!)``.
- ``OTELIZE_SPAN_RETURN_VALUE_IS_INCLUDED``: include return values in spans. Default: ``true``.
