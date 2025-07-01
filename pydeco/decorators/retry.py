from typing import Callable, Sequence

def retry(
        times: int, 
        exceptions: tuple[Exception] = (Exception),
        delay: float = 0,
        backoff_multiplier: float = 0,
        delay_cap: float = 0,
        jitter: float = 0,
        callback: Callable = None,
) -> Callable:

    def dec(fn: Callable):
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs):
            for i in range(times - 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    callback() if callback else None
                    
            return fn(*args, **kwargs)

        return inner
    return dec
