import requests
import pytest
from os import environ

# TODO consider moving this functionality into the proxygen cli


@pytest.mark.run(order=1)
def test_ping(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    assert resp.status_code == 200


@pytest.mark.run(order=2)
def test_wait_for_ping(nhsd_apim_proxy_url):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    deployed_spec_hash = resp.json().get("spec_hash")

    while (
        deployed_spec_hash != environ["SPEC_HASH"]
        and retries <= 30
        and resp.status_code == 200
    ):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
        deployed_spec_hash = resp.json().get("spec_hash")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_spec_hash == environ["SPEC_HASH"]


@pytest.mark.run(order=3)
def test_status(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers={"apikey": environ["STATUS_ENDPOINT_API_KEY"]}
    )
    assert resp.status_code == 200
    # Make some additional assertions about your status response here!


@pytest.mark.run(order=4)
def test_wait_for_status(nhsd_apim_proxy_url):
    retries = 0
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers={"apikey": environ["STATUS_ENDPOINT_API_KEY"]}
    )
    deployed_spec_hash = resp.json().get("spec_hash")

    while (
        deployed_spec_hash != environ["SPEC_HASH"]
        and retries <= 30
        and resp.status_code == 200
        and resp.json().get("version")
    ):
        resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers={"apikey": environ["STATUS_ENDPOINT_API_KEY"]}
        )
        deployed_spec_hash = resp.json().get("spec_hash")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")
    elif not resp.json().get("version"):
        pytest.fail("version not found")

    assert deployed_spec_hash == environ["SPEC_HASH"]
