"""Tests for the frozen_instance decorator."""

import pytest

from classicle import frozen_instance


def test_basic_usage():
    """Test basic usage of frozen_instance decorator."""

    @frozen_instance
    class Config:
        HOST = "localhost"
        PORT = 8080
        DEBUG = True

    # Check that attributes are accessible
    assert Config.HOST == "localhost"
    assert Config.PORT == 8080
    assert Config.DEBUG is True


def test_with_type_hints():
    """Test frozen_instance with type hints."""

    @frozen_instance
    class TypedConfig:
        HOST: str = "localhost"
        PORT: int = 8080
        DEBUG: bool = True

    assert TypedConfig.HOST == "localhost"
    assert TypedConfig.PORT == 8080
    assert TypedConfig.DEBUG is True


def test_dict_conversion():
    """Test that dict(instance) works correctly."""

    @frozen_instance
    class Config:
        HOST = "localhost"
        PORT = 8080
        DEBUG = True

    config_dict = dict(Config)
    assert config_dict == {
        "HOST": "localhost",
        "PORT": 8080,
        "DEBUG": True,
    }


def test_iterable():
    """Test that the instance is iterable."""

    @frozen_instance
    class Config:
        A = 1
        B = 2
        C = 3

    items = list(Config)
    assert len(items) == 3
    assert ("A", 1) in items
    assert ("B", 2) in items
    assert ("C", 3) in items


def test_immutable_attributes():
    """Test that attributes cannot be modified after creation."""

    @frozen_instance
    class Config:
        HOST = "localhost"
        PORT = 8080

    with pytest.raises(AttributeError, match="Cannot modify attribute"):
        Config.HOST = "newhost"


def test_cannot_delete_attributes():
    """Test that attributes cannot be deleted."""

    @frozen_instance
    class Config:
        HOST = "localhost"
        PORT = 8080

    with pytest.raises(AttributeError, match="Cannot delete attribute"):
        del Config.HOST


def test_excludes_private_attributes():
    """Test that private attributes are not included."""

    @frozen_instance
    class Config:
        PUBLIC = "public"
        _PRIVATE = "private"
        __DUNDER = "dunder"

    config_dict = dict(Config)
    assert "PUBLIC" in config_dict
    assert "_PRIVATE" not in config_dict
    assert "__DUNDER" not in config_dict


def test_excludes_methods():
    """Test that methods are not included in the frozen instance."""

    @frozen_instance
    class Config:
        VALUE = 42

        def method(self) -> str:
            return "test"

    config_dict = dict(Config)
    assert "VALUE" in config_dict
    assert "method" not in config_dict


def test_repr():
    """Test the string representation of frozen instance."""

    @frozen_instance
    class Config:
        HOST = "localhost"
        PORT = 8080

    repr_str = repr(Config)
    assert "Config" in repr_str
    assert "HOST='localhost'" in repr_str
    assert "PORT=8080" in repr_str


def test_multiple_instances_are_same():
    """Test that the decorator creates a singleton-like instance."""

    @frozen_instance
    class Config:
        VALUE = 42

    # The decorator returns an instance, not a class
    # So we can't instantiate it again, but we can verify it's an instance
    assert hasattr(Config, "VALUE")
    assert Config.VALUE == 42


def test_empty_class():
    """Test frozen_instance with an empty class."""

    @frozen_instance
    class EmptyConfig:
        pass

    config_dict = dict(EmptyConfig)
    assert config_dict == {}


def test_various_types():
    """Test frozen_instance with various attribute types."""

    @frozen_instance
    class Config:
        STRING = "text"
        INTEGER = 42
        FLOAT = 3.14
        BOOLEAN = True
        NONE = None
        LIST = [1, 2, 3]
        DICT = {"key": "value"}
        TUPLE = (1, 2, 3)

    assert Config.STRING == "text"
    assert Config.INTEGER == 42
    assert Config.FLOAT == 3.14
    assert Config.BOOLEAN is True
    assert Config.NONE is None
    assert Config.LIST == [1, 2, 3]
    assert Config.DICT == {"key": "value"}
    assert Config.TUPLE == (1, 2, 3)

    config_dict = dict(Config)
    assert len(config_dict) == 8
