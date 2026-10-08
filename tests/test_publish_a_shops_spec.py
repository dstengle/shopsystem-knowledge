from pytest_bdd import given, scenarios

from spec_shop import build
from publish_spec_index import *  # noqa: F403  pytest-bdd registers steps only through a star import
from publish_spec_capabilities import *  # noqa: F403
from publish_spec_decisions import *  # noqa: F403
from publish_spec_features import *  # noqa: F403
from publish_spec_from import *  # noqa: F403
from publish_spec_refused import *  # noqa: F403

scenarios("publish-a-shops-spec.feature")


@given(
    "a knowledge base holding a product and a shop of that product, active capabilities linking to the shop each carrying "
    "an order of its own, decisions linking to the shop each carrying a number of its own, and a feature formulating "
    "each capability",
    target_fixture="built",
)
def _a_shop(env, started_shop, tmp_path):
    return build(env, tmp_path)
