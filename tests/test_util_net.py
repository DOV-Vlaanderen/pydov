"""Module grouping tests for the pydov.util.net module."""

import pydov


class TestSessionFactory(object):
    """Class grouping tests for the pydov.util.net.SessionFactory class."""

    def test_user_agent(self):
        """Test the user-agent header of the pydov session.

        Test whether the user-agent header is present and starts with 'pydov-tests'.

        """
        assert "user-agent" in pydov.session.headers
        assert pydov.session.headers["user-agent"].startswith("pydov-tests")
