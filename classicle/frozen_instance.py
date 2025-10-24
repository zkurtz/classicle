"""Frozen instance decorator for creating immutable constant namespaces."""

from typing import Any, Iterator, Tuple


def frozen_instance(cls: type) -> Any:
    """A class decorator that defines the class as already-instantiated and non-instantiable.

    The decorated class:
    - Is immediately instantiated
    - Cannot be instantiated again
    - Has optionally type-hinted class attributes
    - Is iterable, allowing `dict(instance)` to work

    Args:
        cls: The class to decorate

    Returns:
        A single instance of the class that is iterable

    Example:
        >>> @frozen_instance
        ... class Config:
        ...     HOST: str = "localhost"
        ...     PORT: int = 8080
        ...     DEBUG: bool = True
        >>>
        >>> Config.HOST
        'localhost'
        >>> dict(Config)
        {'HOST': 'localhost', 'PORT': 8080, 'DEBUG': True}
    """
    # Get all class attributes (excluding special methods and private attributes)
    attrs = {name: value for name, value in cls.__dict__.items() if not name.startswith("_") and not callable(value)}

    # Create a wrapper class that stores the attributes and makes the instance iterable
    class FrozenInstance:
        def __init__(self) -> None:
            # Copy all public class attributes to the instance
            for name, value in attrs.items():
                object.__setattr__(self, name, value)

        def __iter__(self) -> Iterator[Tuple[str, Any]]:
            """Make the instance iterable for dict() conversion."""
            for name in attrs:
                yield (name, attrs[name])

        def __setattr__(self, name: str, value: Any) -> None:
            """Prevent modification of attributes after initialization."""
            if hasattr(self, name):
                raise AttributeError(f"Cannot modify attribute '{name}' on frozen instance")
            object.__setattr__(self, name, value)

        def __delattr__(self, name: str) -> None:
            """Prevent deletion of attributes."""
            raise AttributeError(f"Cannot delete attribute '{name}' on frozen instance")

        def __repr__(self) -> str:
            """Return a string representation of the frozen instance."""
            items = ", ".join(f"{k}={v!r}" for k, v in self)
            return f"{cls.__name__}({items})"

    # Copy the original class name and module information
    FrozenInstance.__name__ = cls.__name__
    FrozenInstance.__qualname__ = cls.__qualname__
    FrozenInstance.__module__ = cls.__module__

    # Create and return the single instance
    return FrozenInstance()
