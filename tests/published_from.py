"""The published-from line a published file carries, as the spec words it, for the steps that compare a whole file with
what it is expected to be. Imported plainly, never star-imported."""
from driver import whole


def markdown(env, name):
    """The line as an HTML comment, naming the artifact and the revision it holds now."""
    return f"<!-- published from the knowledge base: {name}@{whole(env, name)['revision']}; do not edit by hand -->"
