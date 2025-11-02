"""Tests for the FrozenSpace metaclass."""

import pytest

from classicle import FrozenSpace


def test_basic_usage():
    """Test basic usage of FrozenSpace."""

    class Config(FrozenSpace):
        HOST = "localhost"
        PORT = 8080
        DEBUG = True

    # Check that attributes are accessible
    assert Config.HOST == "localhost"
    assert Config.PORT == 8080
    assert Config.DEBUG is True


def test_with_type_hints():
    """Test FrozenSpace with type hints."""

    class TypedConfig(FrozenSpace):
        HOST: str = "localhost"
        PORT: int = 8080
        DEBUG: bool = True

    assert TypedConfig.HOST == "localhost"
    assert TypedConfig.PORT == 8080
    assert TypedConfig.DEBUG is True


def test_dict_conversion():
    """Test that dict(class) works correctly."""

    class Config(FrozenSpace):
        HOST = "localhost"
        PORT = 8080
        DEBUG = True

    config_dict = dict(Config)
    assert config_dict == {
        "HOST": "localhost",
        "PORT": 8080,
        "DEBUG": True,
    }


def test_mapping_protocol():
    """Test that the Mapping protocol works."""

    class Config(FrozenSpace):
        A = 1
        B = 2
        C = 3

    # Test __getitem__
    assert Config["A"] == 1
    assert Config["B"] == 2
    assert Config["C"] == 3

    # Test __len__
    assert len(Config) == 3

    # Test __iter__
    assert set(Config) == {"A", "B", "C"}

    # Test items()
    items = dict(Config.items())
    assert items == {"A": 1, "B": 2, "C": 3}

    # Test keys()
    assert set(Config.keys()) == {"A", "B", "C"}

    # Test values()
    assert set(Config.values()) == {1, 2, 3}


def test_immutable_attributes():
    """Test that attributes cannot be modified after creation."""

    class Config(FrozenSpace):
        HOST = "localhost"
        PORT = 8080

    with pytest.raises(AttributeError, match="Cannot modify attribute"):
        Config.HOST = "newhost"


def test_cannot_delete_attributes():
    """Test that attributes cannot be deleted."""

    class Config(FrozenSpace):
        HOST = "localhost"
        PORT = 8080

    with pytest.raises(AttributeError, match="Cannot delete attribute"):
        del Config.HOST


def test_excludes_private_attributes():
    """Test that private attributes are not included."""

    class Config(FrozenSpace):
        PUBLIC = "public"
        _PRIVATE = "private"
        __DUNDER = "dunder"

    config_dict = dict(Config)
    assert "PUBLIC" in config_dict
    assert "_PRIVATE" not in config_dict
    assert "__DUNDER" not in config_dict


def test_excludes_methods():
    """Test that methods are not included in the frozen namespace."""

    class Config(FrozenSpace):
        VALUE = 42

        def method(self) -> str:
            return "test"

    config_dict = dict(Config)
    assert "VALUE" in config_dict
    assert "method" not in config_dict


def test_repr():
    """Test the string representation of frozen namespace."""

    class Config(FrozenSpace):
        HOST = "localhost"
        PORT = 8080

    repr_str = repr(Config)
    assert "Config" in repr_str
    assert "HOST='localhost'" in repr_str
    assert "PORT=8080" in repr_str


def test_empty_class():
    """Test FrozenSpace with an empty class."""

    class EmptyConfig(FrozenSpace):
        pass

    config_dict = dict(EmptyConfig)
    assert config_dict == {}


def test_various_types():
    """Test FrozenSpace with various attribute types."""

    class Config(FrozenSpace):
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


def test_getitem_missing_key():
    """Test that __getitem__ raises KeyError for missing keys."""

    class Config(FrozenSpace):
        A = 1

    with pytest.raises(KeyError):
        _ = Config["MISSING"]


def test_inheritance():
    """Test that FrozenSpace can be inherited."""

    class BaseConfig(FrozenSpace):
        BASE = "base"

    class DerivedConfig(BaseConfig):
        DERIVED = "derived"

    # Both should be frozen namespaces
    assert dict(BaseConfig) == {"BASE": "base"}
    assert dict(DerivedConfig) == {"DERIVED": "derived"}


def test_no_instantiation_needed():
    """Test that FrozenSpace works without instantiation."""

    class Config(FrozenSpace):
        VALUE = 42

    # The class itself is the namespace
    assert Config.VALUE == 42
    # No need to instantiate
    assert hasattr(Config, "VALUE")


def test_cannot_instantiate():
    """Test that FrozenSpace classes cannot be instantiated."""

    class Config(FrozenSpace):
        VALUE = 42

    with pytest.raises(TypeError, match="Cannot instantiate Config"):
        Config()
