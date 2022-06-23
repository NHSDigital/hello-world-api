import pytest


def pytest_addoption(parser):
    parser.addoption("--service_base_path", action="store", required=True,
                     help="Service base path. Example: hello-world-pr-234")
    parser.addoption("--apigee_env", action="store", required=True, help="Apigee environment")
    parser.addoption("--client_id", action="store", required=True, help="Client ID of default app")
    parser.addoption("--api_key", action="store", required=True, help="API Key for default app")
    parser.addoption("--status_api_key", action="store", required=True, help="API Key for _status endpoint")
    parser.addoption("--jwt_private_key_file", action="store", required=True, help="Path to private key to sign JWT")
    parser.addoption("--id_token_private_key_file", action="store", required=True,
                     help="Path to private key to create ID Token")
    parser.addoption("--oauth_token_endpoint", action="store", required=True, help="OAuth token endpoint")


def pytest_configure(config):
    """Validate parameters that comes from environment variables (secrets)"""
    api_key = config.getoption("api_key")
    if api_key == "":
        raise Exception("api_key is empty")

    status_api_key = config.getoption("status_api_key")
    if status_api_key == "":
        raise Exception("status_api_key is empty")


@pytest.fixture()
def config(pytestconfig):
    return {
        "apigee_env": pytestconfig.getoption("apigee_env"),
        "service_base_path": pytestconfig.getoption("service_base_path"),
        "client_id": pytestconfig.getoption("client_id"),
        "api_key": pytestconfig.getoption("api_key"),
        "status_api_key": pytestconfig.getoption("status_api_key"),
        "id_token_private_key_file": pytestconfig.getoption("id_token_private_key_file"),
        "jwt_private_key_file": pytestconfig.getoption("jwt_private_key_file"),
        "oauth_token_endpoint": pytestconfig.getoption("oauth_token_endpoint"),
    }


@pytest.fixture()
def service_url(pytestconfig):
    return f'https://{pytestconfig.getoption("apigee_env")}.api.service.nhs.uk' \
           f'/{pytestconfig.getoption("service_base_path")}'
