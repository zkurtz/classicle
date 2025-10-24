# classicle

Immutable constant namespaces with dataclass-like ergonomics.

## Usage

The `frozen_instance` decorator creates an immutable, already-instantiated class that behaves like a constant namespace. This is perfect for configuration objects, constants, and other immutable data structures.

### Basic Example

```python
from classicle import frozen_instance

@frozen_instance
class Config:
    HOST = "localhost"
    PORT = 8080
    DEBUG = True

# Access attributes
print(Config.HOST)  # "localhost"
print(Config.PORT)  # 8080

# Convert to dictionary
config_dict = dict(Config)
# {'HOST': 'localhost', 'PORT': 8080, 'DEBUG': True}

# Iterate over attributes
for name, value in Config:
    print(f"{name} = {value}")
```

### With Type Hints

```python
@frozen_instance
class DatabaseConfig:
    HOST: str = "localhost"
    PORT: int = 5432
    USERNAME: str = "admin"
    PASSWORD: str = "secret"
    DATABASE: str = "mydb"

# Type hints are preserved for static type checkers
print(DatabaseConfig.HOST)  # Type checker knows this is a str
```

### Features

- **Already instantiated**: No need to create an instance, the class itself is the instance
- **Immutable**: Attributes cannot be modified or deleted after creation
- **Iterable**: Works with `dict()`, can be used in for loops
- **Type hints**: Supports optional type hints for better IDE support
- **Clean syntax**: Similar to dataclasses but for constant values
- **No methods included**: Only data attributes are exposed (methods are excluded)
- **No private attributes**: Attributes starting with `_` are not included

### Immutability

```python
@frozen_instance
class Constants:
    PI = 3.14159
    E = 2.71828

# This will raise an AttributeError
try:
    Constants.PI = 3.14
except AttributeError as e:
    print(e)  # "Cannot modify attribute 'PI' on frozen instance"

# This will also raise an AttributeError
try:
    del Constants.E
except AttributeError as e:
    print(e)  # "Cannot delete attribute 'E' on frozen instance"
```

## Installation

Install classicle: We're [on pypi](https://pypi.org/project/classicle/), so `uv add classicle`. If working directly on this repo, consider using the [simplest-possible virtual environment](https://gist.github.com/zkurtz/4c61572b03e667a7596a607706463543).
