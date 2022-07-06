from time import time

import pytest
import requests

from api_tests.helpers import create_jwt


class TestAuthEndpoints:
    @pytest.mark.happy_path
    def test_open_access_api(self, service_url):
        # Given
        endpoint = f"{service_url}/hello/world"

        # When
        response = requests.get(endpoint)

        # Then
        assert response.status_code == 200
        assert "Hello World" in response.text

    @pytest.mark.happy_path
    def test_application_restricted_api_with_api_key(self, config, service_url):
        # Given
        endpoint = f"{service_url}/hello/application"
        api_key = config["api_key"]

        # When
        response = requests.get(endpoint, headers={"apikey": api_key})

        # Then
        assert response.status_code == 200
        assert "Hello Application" in response.text

    @pytest.mark.happy_path
    @pytest.mark.debug
    def test_application_restricted_api_with_client_credentials(self, config, service_url,
                                                                get_token_client_credentials):
        # Given
        endpoint = f"{service_url}/hello/jwt"

        # When
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {get_token_client_credentials}"})

        # Then
        assert response.status_code == 200
        assert "Hello Application" in response.text

    @pytest.mark.happy_path
    def test_user_restricted_api_with_cis2_token_exchange(self, config, service_url):
        # Given
        client_id = config["client_id"]

        client_assertion_claims = {"aud": config["oauth_token_endpoint"]}
        client_assertion_headers = {"kid": "test-1"}
        client_assertion_jwt = create_jwt(private_key_path=config["jwt_private_key_file"], client_id=client_id,
                                          claims=client_assertion_claims, headers=client_assertion_headers)

        id_token_claims = {
            'aud': 'tf_-APIM-1',
            'id_status': 'verified',
            'token_use': 'id',
            'auth_time': 1616600683,
            'iss': 'https://am.nhsint.auth-ptl.cis2.spineservices.nhs.uk:443/openam/oauth2/realms/root/realms/NHSIdentity/realms/Healthcare',
            'vot': 'P9.Cp.Cd',
            'exp': int(time()) + 600,
            'iat': int(time()) - 10,
            'vtm': 'https://auth.sandpit.signin.nhs.uk/trustmark/auth.sandpit.signin.nhs.uk',
            'jti': 'b68ddb28-e440-443d-8725-dfe0da330118',
            "acr": "AAL3_ANY"
        }
        id_token_headers = {
            "sub": "49f470a1-cc52-49b7-beba-0f9cec937c46",
            "aud": "APIM-1",
            "kid": 'identity-service-tests-1',
            "iss": 'https://am.nhsint.auth-ptl.cis2.spineservices.nhs.uk:443/openam/oauth2/realms/root/realms/NHSIdentity/realms/Healthcare',
            "typ": "JWT",
            "exp": 1616604574,
            "iat": 1616600974,
            "alg": "RS512",
            "jti": "b68ddb28-e440-443d-8725-dfe0da330118"
        }
        id_token_jwt = create_jwt(private_key_path=config['id_token_private_key_file'], claims=id_token_claims,
                                  headers=id_token_headers, client_id=client_id)

        post_token_data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
            'subject_token_type': 'urn:ietf:params:oauth:token-type:id_token',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'subject_token': id_token_jwt,
            'client_assertion': client_assertion_jwt
        }
        response = requests.post(config['oauth_token_endpoint'], post_token_data)
        access_token = response.json()['access_token']

        # When
        endpoint = f"{service_url}/hello/user"
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})

        # Then
        assert response.status_code == 200
        assert "Hello User" in response.text
