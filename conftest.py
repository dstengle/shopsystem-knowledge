"""Pytest root conftest.

Keeps ``src/`` importable (``pythonpath = ["src"]`` in pyproject) and marks the
repository root as the rootdir so pytest-bdd resolves ``bdd_features_base_dir``
against ``features/`` regardless of the working directory pytest is invoked
from.
"""
