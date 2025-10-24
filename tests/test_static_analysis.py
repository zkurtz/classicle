"""Tests for static type checking behavior of frozen_instance.

This module verifies that type checkers like mypy can correctly understand
the types of attributes in frozen_instance classes, which is a key selling
point over alternatives like Enum.
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from textwrap import dedent


def _run_mypy(code: str) -> tuple[bool, str]:
    """Run mypy on the provided code and return success status and output.

    Args:
        code: Python code to type check (should only be hardcoded test strings)

    Returns:
        Tuple of (success, output) where success is True if mypy passes
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "test.py"
        temp_file.write_text(code)

        # Use a temporary cache directory to avoid scanning project's .venv
        cache_dir = Path(temp_dir) / ".mypy_cache"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--strict",
                "--no-site-packages",
                "--cache-dir",
                str(cache_dir),
                str(temp_file),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += f"\n--- stderr ---\n{result.stderr}"
        return result.returncode == 0, output


def test_typed_attributes_are_recognized():
    """Test that mypy recognizes the types of typed attributes."""
    code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            HOST: str = "localhost"
            PORT: int = 8080
            DEBUG: bool = True

        # These should be valid according to the type checker
        host: str = Config.HOST
        port: int = Config.PORT
        debug: bool = Config.DEBUG
    """)

    success, output = _run_mypy(code)
    assert success, f"mypy should pass for correctly typed code, but got:\n{output}"


def test_type_errors_are_detected():
    """Test that mypy detects type mismatches."""
    code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            HOST: str = "localhost"
            PORT: int = 8080

        # These should fail type checking
        host: int = Config.HOST  # type: ignore
        port: str = Config.PORT  # type: ignore
    """)

    # We expect this to pass because we're using type: ignore
    # Let's test without the ignore comments
    code_without_ignore = code.replace("  # type: ignore", "")
    success, output = _run_mypy(code_without_ignore)
    assert not success, "mypy should detect type errors"
    assert "error" in output.lower(), f"Expected type error in output:\n{output}"


def test_untyped_attributes_inferred():
    """Test that untyped attributes have their types inferred from values."""
    code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            HOST = "localhost"
            PORT = 8080
            DEBUG = True

        # Type checker should infer types from the assigned values
        host: str = Config.HOST
        port: int = Config.PORT
        debug: bool = Config.DEBUG
    """)

    success, output = _run_mypy(code)
    assert success, f"mypy should infer types from values, but got:\n{output}"


def test_mixed_typed_untyped_attributes():
    """Test classes with both typed and untyped attributes."""
    code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            HOST: str = "localhost"
            PORT = 8080
            DEBUG: bool = True
            TIMEOUT = 30.0

        host: str = Config.HOST
        port: int = Config.PORT
        debug: bool = Config.DEBUG
        timeout: float = Config.TIMEOUT
    """)

    success, output = _run_mypy(code)
    assert success, f"mypy should handle mixed typed/untyped attributes, but got:\n{output}"


def test_complex_types():
    """Test that complex types like lists and dicts are recognized."""
    code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            SERVERS: list[str] = ["server1", "server2"]
            SETTINGS: dict[str, int] = {"max_connections": 100}
            PORTS: tuple[int, ...] = (8080, 8081, 8082)

        servers: list[str] = Config.SERVERS
        settings: dict[str, int] = Config.SETTINGS
        ports: tuple[int, ...] = Config.PORTS
    """)

    success, output = _run_mypy(code)
    assert success, f"mypy should recognize complex types, but got:\n{output}"


def test_none_type():
    """Test that None and Optional types work correctly."""
    code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            HOST: str | None = None
            PORT: int | None = 8080

        host: str | None = Config.HOST
        port: int | None = Config.PORT
    """)

    success, output = _run_mypy(code)
    assert success, f"mypy should handle None types, but got:\n{output}"


def test_comparison_with_enum():
    """Test that frozen_instance provides better type checking than Enum.

    This demonstrates the key selling point: type checkers know the actual types
    of the values, not just that they're enum members.
    """
    # frozen_instance preserves value types
    frozen_code = dedent("""
        from classicle import frozen_instance

        @frozen_instance
        class Config:
            HOST: str = "localhost"
            PORT: int = 8080

        # Can use as typed values
        def connect(host: str, port: int) -> None:
            pass

        connect(Config.HOST, Config.PORT)
    """)

    success, output = _run_mypy(frozen_code)
    assert success, f"frozen_instance should work with typed functions, but got:\n{output}"

    # Enum would require .value access
    enum_code = dedent("""
        from enum import Enum

        class Config(Enum):
            HOST = "localhost"
            PORT = 8080

        # Would need .value to use in typed functions
        def connect(host: str, port: int) -> None:
            pass

        # This would fail type checking without .value
        connect(Config.HOST.value, Config.PORT.value)
    """)

    success, output = _run_mypy(enum_code)
    assert success, f"Enum comparison code should pass with .value, but got:\n{output}"
