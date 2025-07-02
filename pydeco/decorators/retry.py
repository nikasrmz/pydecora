from random import uniform
import time
from typing import Callable, Any, Optional


def retry(
        times: int, 
        exceptions: tuple[type[Exception]] = (Exception,),
        delay: float = 0,
        backoff_multiplier: float = 1,
        delay_cap: float = 30 * 60,
        jitter: float = 0,
        callback: Optional[Callable[[int, Exception], None]] = None,
) -> Callable[..., Any]:

    def dec(fn: Callable[..., Any]) -> Callable:
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs) -> Any:
            current_delay = delay

            for i in range(1, times):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    callback(i, e) if callback else None

                time.sleep(min(current_delay + uniform(0, jitter), delay_cap))
                current_delay *= backoff_multiplier
                    
            return fn(*args, **kwargs)

        return inner
    return dec
