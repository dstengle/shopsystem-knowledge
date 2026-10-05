from pytest_bdd import scenarios

from start_roles_and_tags import *  # noqa: F403  pytest-bdd registers steps only through a star import

scenarios("use-the-shops-types.feature")
