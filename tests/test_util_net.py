"""Module grouping tests for the pydov.util.net module."""

import requests
import urllib3

from pydov.util.net import SessionFactory, TimeoutHTTPAdapter


class TestSessionFactory:
    """Class for testing the SessionFactory."""

    def test_set_user_agent(self):
        """Test the set_user_agent method."""
        session = requests.Session()
        SessionFactory.set_user_agent(session)

        assert session.headers["user-agent"].startswith("pydov-tests")

    def test_get_fail_fast_session(self):
        """Test the get_fail_fast_session method."""
        session = SessionFactory.get_fail_fast_session()

        assert isinstance(session, requests.Session)
        assert "user-agent" in session.headers
        assert session.headers["user-agent"].startswith("pydov-tests")

        # Check if the adapter is correctly configured for timeout and no retries
        for proto in ["http://", "https://"]:
            adapter = session.get_adapter(proto)
            assert isinstance(adapter, TimeoutHTTPAdapter)
            assert adapter.timeout == 10
            assert adapter.max_retries.total == 0

    def test_get_session(self):
        """Test the get_session method."""
        session = SessionFactory.get_session()

        assert isinstance(session, requests.Session)
        assert "user-agent" in session.headers
        assert session.headers["user-agent"].startswith("pydov-tests")

        # Check if the adapter is correctly configured for timeout and retries
        for proto in ["http://", "https://"]:
            adapter = session.get_adapter(proto)
            assert isinstance(adapter, TimeoutHTTPAdapter)
            assert adapter.timeout == 300
            assert isinstance(adapter.max_retries, urllib3.util.Retry)
            assert adapter.max_retries.total == 10
            assert adapter.max_retries.connect == 10
            assert adapter.max_retries.read == 10
            assert adapter.max_retries.redirect == 5
            assert adapter.max_retries.backoff_factor == 1
            if hasattr(adapter.max_retries, "allowed_methods"):
                assert adapter.max_retries.allowed_methods == set(
                    ["HEAD", "GET", "POST", "PUT", "OPTIONS"]
                )
            else:
                assert adapter.max_retries.method_whitelist == set(
                    ["HEAD", "GET", "POST", "PUT", "OPTIONS"]
                )
