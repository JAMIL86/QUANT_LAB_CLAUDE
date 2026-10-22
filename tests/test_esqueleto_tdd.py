"""TDD — Ticket 1."""
import os
def test_pyproject_exists():
    assert os.path.exists('pyproject.toml'), "Ticket 1: pyproject.toml nao existe"
