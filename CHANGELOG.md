# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.4.0 (2025-09-14)
### Features
- Add parameters to positional-only arguments.

### Fixes
- Refactor otelize.py and simplify code for otelize decorator.
- Minor improvements in the README.md.
- Add test to make it clear we are not dealing with exceptions here, we rely on the behavior from the OpenTelemetry library.

## 0.3.0 (2025-09-14)
### Features
- New otelize_context_manager that returns span, and original the context manager result.

## 0.2.0 (2025-09-11)
### Features
- New otelize_iterable that yields span, item for iterables.

### Fixes
- The project now follows the DDD approach.

## 0.1.1 (2025-09-06)
### Fixes
 - New official [documentation page](https://otelize.readthedocs.io/en/latest/) available.

## 0.1.0 (2025-09-05)
### Features
 - `@otelize` now works at class-level, decorating all non-magical methods (including class methods and static methods).

## 0.0.2 (2025-08-30)
First release of the package.

## 0.0.1 (2025-08-30)
### Features
- `@otelize` function decorator that adds automatic OTEL instrumentation to a function.