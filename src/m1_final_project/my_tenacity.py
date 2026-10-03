import logging

logger = logging.getLogger(__name__)
from tenacity import retry, stop_after_attempt, wait_random_exponential


def log_before_retry(retry_state):
    exc = retry_state.outcome.exception()

    logger.warning(
        "Retrying request... | " "attempt=%s | exception=%s | message=%s",
        retry_state.attempt_number,
        type(exc).__name__,
        exc,
    )

    print(f"{type(exc).__name__}: Retrying request...")


def handle_retries_exhausted(retry_state):
    exc = retry_state.outcome.exception()

    logger.error(
        "Retries exhausted | " "attempts=%s | exception=%s | message=%s",
        retry_state.attempt_number,
        type(exc).__name__,
        exc,
    )

    raise exc

    retry = (retry_if_exception_type(retriable_errors),)


# INFO: This would be considered a wrapping decorator, since we're receiving the `retry` and returning a `retry`
# (not transforming it) but with some configurations.
def standard_retry(**kwargs):
    """
    A base retry decorator that accepts overrides.
    """

    # 1. Define your baseline configuration
    defaults = {
        "wait": wait_random_exponential(multiplier=1, min=1, max=60),
        "stop": stop_after_attempt(3),
        "before_sleep": log_before_retry,
        "retry_error_callback": handle_retries_exhausted,
    }

    # 2. Merge overrides into defaults (kwargs takes precedence)
    config = {**defaults, **kwargs}

    # 3. Return a decorator function
    def decorator(fn):
        return retry(**config)(fn)

    return decorator
