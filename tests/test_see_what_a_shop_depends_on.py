from pytest_bdd import scenarios

from dependencies_steps import *  # noqa: F403  pytest-bdd registers steps only through a star import

scenarios("see-what-a-shop-depends-on.feature")
