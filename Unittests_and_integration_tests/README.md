# Unittests_and_integration_tests

Unit and integration tests for `utils.py` and `client.py`, built task-by-task (0–8):

0. `TestAccessNestedMap.test_access_nested_map` — parameterized, `assertEqual`
1. `TestAccessNestedMap.test_access_nested_map_exception` — parameterized,
   `assertRaises`, checks the exception message
2. `TestGetJson.test_get_json` — mocks `requests.get` so no real HTTP call
   is made; checks it's called once per input with the right URL
3. `TestMemoize.test_memoize` — mocks the underlying method and checks it's
   only called once even though the memoized property is accessed twice
4. `TestGithubOrgClient.test_org` — `@patch` as a decorator + `@parameterized.expand`
5. `TestGithubOrgClient.test_public_repos_url` — mocks the `org` property
   via `patch` as a context manager
6. `TestGithubOrgClient.test_public_repos` — mocks `get_json` and
   `_public_repos_url` together
7. `TestGithubOrgClient.test_has_license` — parameterized static-method test
8. `TestIntegrationGithubOrgClient` — integration test using
   `@parameterized_class` and fixtures from `fixtures.py`; only
   `requests.get` is mocked (via `setUpClass`/`tearDownClass`), everything
   else runs for real

## Setup

```
pip3 install -r requirements.txt
```

## Run the tests

```
python3 -m unittest discover -v
```

or individually:

```
python3 -m unittest test_utils -v
python3 -m unittest test_client -v
```

## Files

- `utils.py` / `client.py` / `fixtures.py` — the modules under test
  (`fixtures.py` holds the `org_payload`, `repos_payload`, `expected_repos`,
  and `apache2_repos` sample data used by the integration test)
- `test_utils.py` — tasks 0–3
- `test_client.py` — tasks 4–8
