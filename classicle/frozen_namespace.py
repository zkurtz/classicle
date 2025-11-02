"""Metaclass-based frozen namespace implementation."""

import abc
from collections.abc import Mapping
from typing import Any, Iterator


class _FrozenSpaceMetaMeta(abc.ABCMeta):
    """Metaclass for FrozenSpaceMeta that fixes ABC machinery issues.

    When FrozenSpaceMeta (which inherits from both type and Mapping) is checked
    by ABC's __subclasscheck__, it tries to access __subclasses__() which fails.
    This metaclass overrides __subclasscheck__ to use type's behavior instead of
    ABCMeta's for FrozenSpaceMeta itself, while allowing normal ABC behavior
    for instances of FrozenSpaceMeta.
    """

    def __subclasscheck__(cls, subclass: type) -> bool:
        """Check if subclass is a subclass of cls.

        Args:
            subclass: The class to check

        Returns:
            True if subclass is a subclass of cls
        """
        # If cls is FrozenSpaceMeta, use type's __subclasscheck__ to avoid
        # ABCMeta's machinery which tries to access __subclasses__()
        if cls.__name__ == "FrozenSpaceMeta":
            return type.__subclasscheck__(cls, subclass)
        # Otherwise use ABCMeta's default behavior
        return super().__subclasscheck__(subclass)


class FrozenSpaceMeta(type, Mapping[str, Any], metaclass=_FrozenSpaceMetaMeta):
    """Metaclass that makes the class itself act as a frozen mapping.

    This allows the class to be used directly without instantiation,
    and makes it compatible with dict() and type checkers.
    """

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        """Create a new frozen namespace class.

        Args:
            mcs: The metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary

        Returns:
            A new class that acts as a frozen namespace
        """
        # Extract only public non-callable attributes (constants)
        attrs = {k: v for k, v in namespace.items() if not k.startswith("_") and not callable(v)}

        # Create new namespace with only essential items
        new_namespace = {
            "__attrs__": attrs,
            "__module__": namespace.get("__module__", ""),
            "__qualname__": namespace.get("__qualname__", name),
            "__doc__": namespace.get("__doc__"),
            "__annotations__": namespace.get("__annotations__", {}),
        }

        cls = super().__new__(mcs, name, bases, new_namespace)
        return cls

    def __iter__(cls) -> Iterator[str]:
        """Iterate over attribute names.

        Returns:
            Iterator over attribute names
        """
        return iter(cls.__attrs__)

    def __len__(cls) -> int:
        """Return number of attributes.

        Returns:
            Number of attributes in the namespace
        """
        return len(cls.__attrs__)

    def __getitem__(cls, key: str) -> Any:
        """Get attribute value by name (mapping protocol).

        Args:
            key: Attribute name

        Returns:
            Attribute value

        Raises:
            KeyError: If attribute not found
        """
        if key in cls.__attrs__:
            return cls.__attrs__[key]
        raise KeyError(key)

    def __hash__(cls) -> int:
        """Return hash of the class.

        Restores hashability which is needed for ABC checks and other Python internals.
        Mapping sets __hash__ = None, but we need classes to be hashable.

        Returns:
            Hash value for the class
        """
        return type.__hash__(cls)

    def __getattribute__(cls, name: str) -> Any:
        """Get attribute value by name (attribute access).

        This checks __attrs__ first for public attributes, allowing
        both mapping-style and attribute-style access.

        Args:
            name: Attribute name

        Returns:
            Attribute value
        """
        # Let all dunder methods go through normal resolution
        # This ensures Python's internal mechanisms (ABC checks, etc.) work correctly
        if name.startswith("__") and name.endswith("__"):
            return super().__getattribute__(name)

        # Check if it's one of our frozen attributes
        try:
            attrs = super().__getattribute__("__attrs__")
            if name in attrs:
                return attrs[name]
        except AttributeError:
            pass

        # Fall back to normal attribute resolution (for methods, etc.)
        return super().__getattribute__(name)

    def __setattr__(cls, name: str, value: Any) -> None:
        """Prevent modification of attributes.

        Args:
            name: Attribute name
            value: New value

        Raises:
            AttributeError: Always, as namespace is frozen
        """
        # Allow internal attributes during class creation
        if name in ("__attrs__", "__module__", "__qualname__", "__doc__", "__annotations__"):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Cannot modify attribute '{name}' on frozen namespace")

    def __delattr__(cls, name: str) -> None:
        """Prevent deletion of attributes.

        Args:
            name: Attribute name

        Raises:
            AttributeError: Always, as namespace is frozen
        """
        raise AttributeError(f"Cannot delete attribute '{name}' on frozen namespace")

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        """Prevent instantiation of FrozenSpace classes.

        Args:
            *args: Positional arguments (ignored)
            **kwargs: Keyword arguments (ignored)

        Raises:
            TypeError: Always, as FrozenSpace classes cannot be instantiated
        """
        raise TypeError(
            f"Cannot instantiate {cls.__name__}. FrozenSpace classes are used directly without instantiation."
        )

    def __repr__(cls) -> str:
        """Return string representation.

        Returns:
            String representation of the frozen namespace
        """
        items = ", ".join(f"{k}={v!r}" for k, v in cls.items())
        return f"{cls.__name__}({items})"


class FrozenSpace(metaclass=FrozenSpaceMeta):
    """Base class for frozen constant namespaces.

    Classes inheriting from FrozenSpace become frozen, immutable namespaces
    that can be used without instantiation. They work seamlessly with type checkers
    and support mapping operations like dict() conversion.

    Example:
        >>> class Config(FrozenSpace):
        ...     HOST: str = "localhost"
        ...     PORT: int = 8080
        ...     DEBUG: bool = True
        ...
        >>> Config.HOST
        'localhost'
        >>> dict(Config)
        {'HOST': 'localhost', 'PORT': 8080, 'DEBUG': True}
        >>> for name, value in Config.items():
        ...     print(f"{name} = {value}")
        HOST = localhost
        PORT = 8080
        DEBUG = True
    """

    pass
