#!/usr/bin/env python3
"""Fixtures for the TestIntegrationGithubOrgClient class testing.
"""

org_payload = {
    "login": "google",
    "id": 1342004,
    "url": "https://api.github.com/orgs/google",
    "repos_url": "https://api.github.com/orgs/google/repos",
}

repos_payload = [
    {
        "id": 7697149,
        "name": "episodes.dart",
        "license": {"key": "bsd-3-clause"},
    },
    {
        "id": 7776515,
        "name": "cpp-netlib",
        "license": {"key": "bsl-1.0"},
    },
    {
        "id": 7968417,
        "name": "dagger",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 8165161,
        "name": "ios-webkit-debug-proxy",
        "license": {"key": "bsd-3-clause"},
    },
    {
        "id": 8459994,
        "name": "google.github.io",
        "license": None,
    },
    {
        "id": 8566972,
        "name": "kratu",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 8858648,
        "name": "build-debian-cloud",
        "license": None,
    },
    {
        "id": 9060347,
        "name": "traceur-compiler",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 9065917,
        "name": "firmata.py",
        "license": {"key": "apache-2.0"},
    },
]

expected_repos = [
    "episodes.dart",
    "cpp-netlib",
    "dagger",
    "ios-webkit-debug-proxy",
    "google.github.io",
    "kratu",
    "build-debian-cloud",
    "traceur-compiler",
    "firmata.py",
]

apache2_repos = [
    "dagger",
    "kratu",
    "traceur-compiler",
    "firmata.py",
]

TEST_PAYLOAD = [
    (org_payload, repos_payload, expected_repos, apache2_repos),
]
