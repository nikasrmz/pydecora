# pydecora

[![PyPI version](https://img.shields.io/pypi/v/pydecora)](https://pypi.org/project/pydecora/)  
A lightweight and modular Python decorator library that provides useful, production-ready decorators for common development patterns. Built with performance and simplicity in mind.

## Features

- **cache**: Smart in-memory caching with TTL, size limits, and LRU eviction
- **retry**: Robust retry mechanism with exponential backoff, jitter, and custom callbacks
- **suppress**: Exception suppression with optional logging and default values
- **timeit**: Execution timing with configurable logging and units
- **validate_args**: Runtime type validation for function arguments and return values
- **singleton**: Classic singleton pattern implementation for classes

## Quick Start

### Installation

```bash
pip install pydecora
```

### Basic Usage

```python
from pydecora import cache, retry, timeit, validate_args, suppress, singleton

# Cache expensive computations
@cache(ttl=300, max_size=100)
def expensive_calculation(x, y):
    return x ** y + complex_operation()

# Retry with exponential backoff
@retry(times=3, delay=1, backoff_multiplier=2)
def unreliable_api_call():
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()

# Time function execution
@timeit(log_args=True, unit="ms")
def process_data(data):
    return [item.upper() for item in data]

# Validate function arguments
@validate_args(check_return=True)
def calculate_distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

# Suppress specific exceptions
@suppress(ValueError, default_value=0, log=True)
def safe_int_conversion(value):
    return int(value)

# Singleton pattern
@singleton
class DatabaseConnection:
    def __init__(self):
        self.connection = create_connection()
```

## Detailed Documentation

### cache

Smart caching decorator with multiple eviction strategies.

```python
@cache(max_size=128, ttl=3600, typed=True)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Parameters:**
- `max_size` (int, optional): Maximum cache size. Uses LRU eviction when exceeded.
- `ttl` (float, optional): Time-to-live in seconds. Items expire after this duration.
- `typed` (bool): If `True`, arguments of different types are cached separately (e.g., `1` vs `1.0`).

### retry

Robust retry mechanism for handling transient failures.

```python
@retry(
    times=5,
    exceptions=(requests.RequestException, ConnectionError),
    delay=1,
    backoff_multiplier=2,
    delay_cap=60,
    jitter=0.1,
    callback=lambda attempt, exc: logger.warning(f"Attempt {attempt} failed: {exc}")
)
def fetch_data():
    return requests.get("https://api.example.com").json()
```

**Parameters:**
- `times` (int): Total number of attempts (including initial call).
- `exceptions` (tuple): Exception types to catch and retry on.
- `delay` (float): Initial delay between retries in seconds.
- `backoff_multiplier` (float): Multiplier for exponential backoff.
- `delay_cap` (float): Maximum delay between retries.
- `jitter` (float): Maximum random jitter to add to delays.
- `callback` (callable, optional): Function called on each failure with `(attempt, exception)`.

### suppress

Exception suppression with optional logging and default values.

```python
@suppress(
    exceptions=(ValueError, TypeError),
    default_value=None,
    log=True,
    log_level=logging.WARNING
)
def parse_config_value(value):
    return json.loads(value)
```

**Parameters:**
- `exceptions`: Exception or tuple of exceptions to suppress.
- `default_value`: Value to return when an exception is suppressed.
- `log` (bool): Whether to log suppressed exceptions.
- `log_level` (int): Logging level for suppression messages.

### timeit

Execution timing with flexible logging options.

```python
@timeit(
    label="Data Processing",
    log_args=True,
    log_result=False,
    log_level=logging.INFO,
    unit="ms"
)
def process_large_dataset(data, threshold=0.5):
    return [item for item in data if item.score > threshold]
```

**Parameters:**
- `label` (str, optional): Custom label for log messages (defaults to function name).
- `log_args` (bool): Include function arguments in log output.
- `log_result` (bool): Include return value in log output.
- `log_level` (int): Logging level for timing messages.
- `unit` (str): Time unit - either `"s"` (seconds) or `"ms"` (milliseconds).

### validate_args

Runtime type validation for function arguments and return values.

```python
from typing import List, Dict, Optional, Union

@validate_args(
    check_return=True,
    exclusions=["self"],
    strict=False,
    warn_only=False
)
def process_users(
    users: List[Dict[str, Union[str, int]]],
    active_only: bool = True
) -> List[str]:
    return [user["name"] for user in users if not active_only or user.get("active", True)]
```

**Parameters:**
- `check_return` (bool): Validate return value against return annotation.
- `raise_exception` (Exception): Exception type to raise on validation failure.
- `exclusions` (iterable): Argument names to skip validation (useful for `self`).
- `strict` (bool): Use exact type matching instead of `isinstance` checks.
- `warn_only` (bool): Log warnings instead of raising exceptions.

**Supported Types:**
- Basic types: `int`, `str`, `float`, `bool`, etc.
- Generic types: `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[T, ...]`
- Union types: `Union[int, str]`, `Optional[int]`
- Nested generics: `List[Dict[str, Optional[int]]]`
- Fixed tuples: `Tuple[int, str, float]`

### singleton

Classic singleton pattern for ensuring single instance classes.

```python
@singleton
class ApplicationConfig:
    def __init__(self, config_file="app.json"):
        self.settings = self.load_config(config_file)
        self.initialized_at = time.time()
    
    def load_config(self, file_path):
        with open(file_path) as f:
            return json.load(f)

# All instances return the same object
config1 = ApplicationConfig()
config2 = ApplicationConfig("different.json")  # Still returns config1
assert config1 is config2  # True
```

## Testing

Run the test suite:

```bash
# Install development dependencies
pip install pytest

# Run tests
pytest tests/

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=pydecora --cov-report=html
```

## Project Structure

```
pydecora/
├── pydecora/
│   ├── __init__.py
│   └── decorators/
│       ├── cache.py           # Caching decorator
│       ├── retry.py           # Retry mechanism
│       ├── singleton.py       # Singleton pattern
│       ├── suppress.py        # Exception suppression
│       ├── timeit.py          # Execution timing
│       └── validate_args.py   # Type validation
├── tests/                     # Comprehensive test suite
├── README.md
├── LICENSE
└── pyproject.toml
```

## Contributing

We welcome contributions! Please feel free to:

1. **Report Issues**: Found a bug or have a feature request? Open an issue on GitHub
2. **Submit Pull Requests**: Fork the repository and submit a PR
3. **Improve Documentation**: Help make our docs even better
4. **Add Tests**: More test coverage is always appreciated

### Development Setup

```bash
# Clone the repository
git clone https://github.com/nikasrmz/pydecora.git
cd pydecora

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

## Requirements

- Python 3.6+
- No external dependencies (uses only Python standard library)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- PyPI: https://pypi.org/project/pydecora/
- GitHub: https://github.com/nikasrmz/pydecora