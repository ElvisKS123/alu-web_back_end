#!/usr/bin/env python3
"""Unit and integration tests for the client module.
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value and
        that get_json is called once with the expected URL, without
        making any actual external HTTP call.
        """
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the repos_url found in
        the (mocked) org payload.
        """
        known_payload = {"repos_url": "http://example.com/repos"}

        with patch.object(
                GithubOrgClient, "org",
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

        self.assertEqual(result, known_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo
        names, and that the mocked property and get_json were each
        called once.
        """
        test_payload = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
                GithubOrgClient, "_public_repos_url",
                new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://example.com/repos"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            mock_url.assert_called_once()

        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_get_json.assert_called_once_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly determines whether a repo
        has the given license key.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD,
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos.

    Only external HTTP calls (requests.get) are mocked; everything else
    runs for real.
    """

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return example payloads based on URL,
        for the duration of this test class.
        """
        route_payload = {
            GithubOrgClient.ORG_URL.format(org="google"): cls.org_payload,
            cls.org_payload["repos_url"]: cls.repos_payload,
        }

        def get_payload(url):
            """Return a Mock whose .json() yields the fixture payload
            matching the requested URL.
            """
            if url in route_payload:
                mock_response = Mock()
                mock_response.json.return_value = route_payload[url]
                return mock_response
            raise ValueError(f"Unhandled URL in test: {url}")

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher started in setUpClass.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repo
        names, using only the mocked external HTTP calls.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters correctly by license when
        given the "apache-2.0" license key.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )


if __name__ == "__main__":
    unittest.main()
