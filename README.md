# classicle

Provides immutable constant namespaces with dataclass-like ergonomics. See the [Python discussion thread](https://discuss.python.org/t/constants-namespace-with-dataclass-like-features/91547) for context, motivation, and alternative approaches.

## Usage

The `FrozenSpace` base class creates frozen namespaces that work perfectly with type checkers like mypy, pyright, and ty. No `type: ignore` comments needed!

### Basic Example

```python
from classicle import FrozenSpace

class Config(FrozenSpace):
    HOST = "localhost"
    PORT = 8080
    DEBUG = True

# Access attributes
print(Config.HOST)  # "localhost"
print(Config.PORT)  # 8080

# Convert to dictionary - works without type: ignore!
config_dict = dict(Config)
# {'HOST': 'localhost', 'PORT': 8080, 'DEBUG': True}

# Iterate over attributes
for name, value in Config.items():
    print(f"{name} = {value}")
```

### With Type Hints

```python
class DatabaseConfig(FrozenSpace):
    HOST: str = "localhost"
    PORT: int = 5432
    USERNAME: str = "admin"
    PASSWORD: str = "secret"
    DATABASE: str = "mydb"

# Type hints are preserved for static type checkers
print(DatabaseConfig.HOST)  # Type checker knows this is a str
```

### Features

- **Type checker friendly**: Works with mypy, pyright, ty without `type: ignore` comments
- **No instantiation needed**: The class itself is the namespace (cannot be instantiated)
- **Immutable**: Attributes cannot be modified or deleted after creation
- **Mapping protocol**: Supports `dict()`, `len()`, `in`, iteration, `.items()`, `.keys()`, `.values()`
- **Type hints**: Full support for type hints
- **Clean syntax**: Similar to dataclasses but for constant values
- **No methods included**: Only data attributes are exposed
- **No private attributes**: Attributes starting with `_` are not included

### Immutability

```python
class Constants(FrozenSpace):
    PI = 3.14159
    E = 2.71828

# This will raise an AttributeError
try:
    Constants.PI = 3.14
except AttributeError as e:
    print(e)  # "Cannot modify attribute 'PI' on frozen namespace"

# This will also raise an AttributeError
try:
    del Constants.E
except AttributeError as e:
    print(e)  # "Cannot delete attribute 'E' on frozen namespace"

# Cannot instantiate FrozenSpace classes
try:
    instance = Constants()
except TypeError as e:
    print(e)  # "Cannot instantiate Constants..."
```

## Installation

Install classicle: We're [on pypi](https://pypi.org/project/classicle/), so `uv add classicle`. If working directly on this repo, consider using the [simplest-possible virtual environment](https://gist.github.com/zkurtz/4c61572b03e667a7596a607706463543).
