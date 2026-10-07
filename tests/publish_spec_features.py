"""The steps of publish-a-shops-spec for the feature files. Star-imported by the feature's test module alone
(adrs/0035)."""
from pytest_bdd import then
from pytest_bdd.parser import FeatureParser

import spec_shop


def parsed(path):
    """The published file as the Gherkin parser the suite uses reads it: its feature, with the scenarios it found."""
    return FeatureParser(str(path.parent), path.name, "utf-8").parse()


@then("that directory holds `features/<name>.feature` for each feature formulating one of the shop's capabilities")
def _holds_each_feature(result, target, built):
    assert result.returncode == 0, result.stderr
    for name, each in zip((capability.split("/", 1)[1] for capability in built.capabilities), spec_shop.CAPABILITIES):
        feature = parsed(target / "features" / f"{name}.feature")
        assert feature.name == each["title"]
        assert [scenario.name for scenario in feature.scenarios.values()] == [f"{each['title']}, as the user does it"]
