from pytest_bdd import scenarios

from formulated_steps import *  # noqa: F403  pytest-bdd registers steps only through a star import

scenarios("see-what-is-formulated.feature")
