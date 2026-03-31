"""Smoke tests for API app wiring."""

from app.main import app


def test_root_route_is_registered() -> None:
    """Test whether root endpoint exists."""
    paths = {route.path for route in app.routes}
    assert "/" in paths
