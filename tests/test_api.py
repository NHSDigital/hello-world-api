import pytest
import requests

from conftest import API_NAME


SESSION = requests.session()


# Helper functions
def _test_endpoint(
    nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code,
):
    # When a request is sent to the proxy at a given path
    resp = SESSION.get(nhsd_apim_proxy_url + f"{path}", headers=nhsd_apim_auth_headers,)
    assert resp.status_code == expected_status_code
    if resp.status_code == 200:
        *_, data = path.split("/")
        assert resp.json()["message"].lower() == f"hello {data}!"


def _test_input(path, expected_status_code, **kwargs):
    kwargs["api_name"] = API_NAME
    return pytest.param(
        path, expected_status_code, marks=pytest.mark.nhsd_apim_authorization(kwargs),
    )


class TestAPI:
    """
    Test Hello World API health and endpoints
    """

    # Test Health endpoints
    def test_ping_endpoint(self, nhsd_apim_proxy_url):
        """
        Send a request to _ping endpoint to test health of proxy.
        """

        resp = SESSION.get(nhsd_apim_proxy_url + "/_ping")
        assert resp.status_code == 200

        # TO DO - Test response once proxygen generates standardised _ping response
        # ping_data = json.loads(resp.text)
        # assert "version" in ping_data

    def test_status_is_secured(self, nhsd_apim_proxy_url):
        """
        Send an unauthenticated request to status to check secured
        """

        resp = SESSION.get(nhsd_apim_proxy_url + "/_status")
        assert resp.status_code == 401

    def test_status_endpoint(self, nhsd_apim_proxy_url, status_endpoint_auth_headers):
        """
        Send a request to the _status endpoint, protected by a platform-wide apikey.
        """

        resp = requests.get(
            nhsd_apim_proxy_url + "/_status", headers=status_endpoint_auth_headers
        )
        status_json = resp.json()
        assert resp.status_code == 200
        assert status_json["status"] == "pass"

        # TO DO - Implement versioning on paas status endpoint so we can 'wait for status'

    # Test Open-access
    @pytest.mark.parametrize(
        "path,expected_status_code",
        [("/hello/user", 401,), ("/hello/application", 401,), ("/hello/world", 200,)],
    )
    def test_open_access(self, nhsd_apim_proxy_url, path, expected_status_code):
        _test_endpoint(nhsd_apim_proxy_url, {}, path, expected_status_code)

    # Test User-restricted access
    @pytest.mark.parametrize(
        "path,expected_status_code",
        [
            # hello/user P9
            _test_input(
                "/hello/user",
                200,
                access="patient",
                level="P9",
                login_form={"auth_method": "P9"},
            ),
            # hello/user P5
            _test_input(
                "/hello/user",
                200,
                access="patient",
                level="P9",
                login_form={"auth_method": "P5"},
            ),
            # hello/application P9
            _test_input(
                path="/hello/application",
                expected_status_code=401,
                access="patient",
                level="P9",
                login_form={"auth_method": "P9"},
            ),
            # hello/application P5
            _test_input(
                "/hello/application",
                401,
                access="patient",
                level="P9",
                login_form={"auth_method": "P5"},
            ),
            # hello/world P9
            _test_input(
                "/hello/world",
                200,
                api_name=API_NAME,
                access="patient",
                level="P9",
                login_form={"auth_method": "P9"},
            ),
            # hello/world P5
            _test_input(
                "/hello/world",
                200,
                api_name=API_NAME,
                access="patient",
                level="P9",
                login_form={"auth_method": "P5"},
            ),
        ],
    )
    def test_user_restricted_nhs_login(
        self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code,
    ):
        _test_endpoint(
            nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code
        )

    @pytest.mark.parametrize(
        "path,expected_status_code",
        [
            # hello/user CIS2 with user 656005750104
            _test_input(
                "/hello/user",
                200,
                api_name=API_NAME,
                access="healthcare_worker",
                level="aal3",
                login_form={"username": "656005750104"},
            ),
            # hello/user CIS2 with user 656005750104
            _test_input(
                "/hello/user",
                200,
                api_name=API_NAME,
                access="healthcare_worker",
                level="aal3",
                login_form={"username": "656005750104"},
            ),
            # hello/application CIS2 with user 656005750104
            _test_input(
                "/hello/application",
                401,
                api_name=API_NAME,
                access="healthcare_worker",
                level="aal3",
                login_form={"username": "656005750104"},
            ),
            # hello/application CIS2 with user 656005750104
            _test_input(
                "/hello/application",
                401,
                api_name=API_NAME,
                access="healthcare_worker",
                level="aal3",
                login_form={"username": "656005750104"},
            ),
            # hello/world CIS2 with user 656005750104
            _test_input(
                "/hello/world",
                200,
                api_name=API_NAME,
                access="healthcare_worker",
                level="aal3",
                login_form={"username": "656005750104"},
            ),
            # hello/world CIS2 with user 656005750104
            _test_input(
                "/hello/world",
                200,
                api_name=API_NAME,
                access="healthcare_worker",
                level="aal3",
                login_form={"username": "656005750104"},
            ),
        ],
    )
    def test_user_restricted_cis2(
        self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code,
    ):
        _test_endpoint(
            nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code
        )

    # Test Application-restricted access
    @pytest.mark.parametrize(
        "path,expected_status_code",
        [
            _test_input(
                "/hello/user",
                401,
                api_name=API_NAME,
                access="application",
                level="level3",
            ),
            _test_input(
                "/hello/application",
                200,
                api_name=API_NAME,
                access="application",
                level="level3",
            ),
            _test_input(
                "/hello/world",
                200,
                api_name=API_NAME,
                access="application",
                level="level3",
            ),
            _test_input(
                "/hello/user",
                401,
                api_name=API_NAME,
                access="application",
                level="level3",
            ),
            _test_input(
                "/hello/application",
                200,
                api_name=API_NAME,
                access="application",
                level="level3",
            ),
            _test_input(
                "/hello/world",
                200,
                api_name=API_NAME,
                access="application",
                level="level3",
            ),
        ],
    )
    def test_app_restricted(
        self, nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code
    ):
        _test_endpoint(
            nhsd_apim_proxy_url, nhsd_apim_auth_headers, path, expected_status_code
        )
