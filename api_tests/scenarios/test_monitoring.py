import pytest
import requests


class TestMonitoringEndpoints:
    @pytest.mark.happy_path
    def test_ping(self, service_url):
        # Given
        endpoint = f"{service_url}/_ping"

        # When
        response = requests.get(endpoint)

        # Then
        assert response.status_code == 200

    @pytest.mark.happy_path
    def test_status(self, config, service_url):
        # Given
        endpoint = f"{service_url}/_status"
        status_api_key = config["status_api_key"]

        # When
        response = requests.get(endpoint, headers={"apikey": status_api_key})

        # Then
        assert response.status_code == 200
