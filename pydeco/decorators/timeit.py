import time
import logging
from typing import Optional, Literal, Callable


def timeit(
    label: Optional[str] = None,
    log_args: bool = False,
    log_result: bool = False,
    log_level: int = logging.INFO,
    unit: Literal["ms", "s"] = "s",
) -> Callable:

    def dec(fn: Callable):
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs):
            if unit not in ("ms", "s"):
                raise ValueError(f"'{unit}' is an unknown unit")

            start = time.perf_counter()
            result = fn(*args, **kwargs)
            end = time.perf_counter()

            name = label or fn.__name__

            if log_args and (args or kwargs):
                args_string = [str(arg) for arg in args]
                kwargs_string = [f"{k}={v}" for k, v in kwargs.items()]
                params_string = f"{', '.join(args_string)}, {', '.join(kwargs_string)}"
            else:
                params_string = ""

            total_time = end - start
            if unit == "ms":
                total_time *= 1000
            result_string = f" and returned: \n {result}" if log_result else ""

            message = (
                f"{name}({params_string}) took {total_time:.7f}{unit}{result_string}"
            )

            logging.log(log_level, message)

            return result

        return inner

    return dec
