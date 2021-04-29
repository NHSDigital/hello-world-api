import pytest


def pytest_addoption(parser):
    parser.addoption("--service_name", action="store", required=True,
                     help="Fully qualified service name. Example: hello-world-pr-234")
    parser.addoption("--apigee_env", action="store", required=True, help="Apigee environment")
    parser.addoption("--client_id", action="store", required=True, help="Client ID of default app")
    parser.addoption("--jwt_private_key_file", action="store", required=True, help="Path to private key to sign JWT")
    parser.addoption("--id_token_private_key_file", action="store", required=True,
                     help="Path to private key to create ID Token")
    parser.addoption("--oauth_token_endpoint", action="store", required=False,
                     default="https://internal-dev.api.service.nhs.uk/oauth2/token", help="OAuth token endpoint")


@pytest.fixture()
def config(pytestconfig):
    return {
        "apigee_env": pytestconfig.getoption("apigee_env"),
        "service_name": pytestconfig.getoption("service_name"),
        "client_id": pytestconfig.getoption("client_id"),
        "id_token_private_key_file": pytestconfig.getoption("id_token_private_key_file"),
        "jwt_private_key_file": pytestconfig.getoption("jwt_private_key_file"),
        "oauth_token_endpoint": pytestconfig.getoption("oauth_token_endpoint"),
    }


@pytest.fixture()
def service_url(pytestconfig):
    return f'https://{pytestconfig.getoption("apigee_env")}.api.service.nhs.uk/{pytestconfig.getoption("service_name")}'
