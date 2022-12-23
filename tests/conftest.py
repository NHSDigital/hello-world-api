import os
import pytest
import requests


SESSION = requests.session()

API_NAME = os.environ["PROXYGEN_API_NAME"]
INSTANCE = os.environ["INSTANCE"]
ENVIRONMENT = os.environ["ENVIRONMENT"]
NAMESPACED_API_NAME = f"{API_NAME}--{ENVIRONMENT}--{INSTANCE}"

# Must have the proxy setup
os.environ["PROXY_NAME"] = NAMESPACED_API_NAME


@pytest.fixture(scope="session")
def nhsd_apim_api_name():
    return API_NAME


@pytest.fixture(scope="session")
def nhsd_apim_proxy_name():
    return NAMESPACED_API_NAME
