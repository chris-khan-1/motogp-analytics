import pytest


def _skip_integration_tests(test: pytest.Function) -> None:
    """Tell `pytest` to skip tests marked as integration."""

    integration_markers = list(test.iter_markers(name="integration"))

    if integration_markers:
        pytest.skip("Skipping integration tests.")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests",
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    if not item.config.getoption("--run-integration"):
        _skip_integration_tests(test=item)
