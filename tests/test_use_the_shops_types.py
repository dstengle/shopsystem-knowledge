from pytest_bdd import scenarios

from start_roles_and_tags import *  # noqa: F403  pytest-bdd registers steps only through a star import
from types_listed_and_read import *  # noqa: F403
from types_common_fields import *  # noqa: F403
from types_process_steps import *  # noqa: F403
from types_spec_kinds import *  # noqa: F403
from types_spec_limits import *  # noqa: F403
from types_capability_links import *  # noqa: F403
from types_spec_scenarios import *  # noqa: F403

scenarios("use-the-shops-types.feature")
