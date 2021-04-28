from time import time
import requests

import pytest

from api_tests.scripts.config import (
    ID_TOKEN_NHS_LOGIN_PRIVATE_KEY_ABSOLUTE_PATH,
    SERVICE_NAME
)

apigee_env = 'internal-dev'
service_url = f'https://{apigee_env}.api.service.nhs.uk/{SERVICE_NAME}'

@pytest.mark.asyncio
class TestOauthEndpoints:
    """ A test suit to verify all the oauth endpoints """

    def _update_secrets(self, request):
        key = ("params", "data")[request.get("params", None) is None]
        if request[key].get("client_id", None) == "/replace_me":
            request[key]["client_id"] = self.oauth.client_id

        if request[key].get("client_secret", None) == "/replace_me":
            request[key]["client_secret"] = self.oauth.client_secret

        if request[key].get("redirect_uri", None) == "/replace_me":
            request[key]["redirect_uri"] = self.oauth.redirect_uri

    @pytest.mark.debug
    @pytest.mark.happy_path
    async def test_nhs_login_happy_path(self):
        # Given
        id_token_claims = {
            'aud': 'tf_-APIM-1',
            'id_status': 'verified',
            'token_use': 'id',
            'auth_time': 1616600683,
            'iss': 'https://internal-dev.api.service.nhs.uk',
            'vot': 'P9.Cp.Cd',
            'exp': int(time()) + 600,
            'iat': int(time()) - 10,
            'vtm': 'https://auth.sandpit.signin.nhs.uk/trustmark/auth.sandpit.signin.nhs.uk',
            'jti': 'b68ddb28-e440-443d-8725-dfe0da330118',
            'identity_proofing_level': 'P9'
        }
        id_token_headers = {
            "sub": "49f470a1-cc52-49b7-beba-0f9cec937c46",
            "aud": "APIM-1",
            "kid": "nhs-login",
            "iss": "https://internal-dev.api.service.nhs.uk",
            "typ": "JWT",
            "exp": 1616604574,
            "iat": 1616600974,
            "alg": "RS512",
            "jti": "b68ddb28-e440-443d-8725-dfe0da330118"
        }

        with open(ID_TOKEN_NHS_LOGIN_PRIVATE_KEY_ABSOLUTE_PATH, "r") as f:
            contents = f.read()

        client_assertion_jwt = self.oauth.create_jwt(kid="test-1", client_id='eAMbFALgZFdnds2w5Z1u78AGCcJ0FtxQ')
        id_token_jwt = self.oauth.create_id_token_jwt(algorithm='RS512', claims=id_token_claims,
                                                      headers=id_token_headers, signing_key=contents)

        resp = await self.oauth.get_token_response(
            grant_type="token_exchange",
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
                'subject_token_type': 'urn:ietf:params:oauth:token-type:id_token',
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'subject_token': id_token_jwt,
                'client_assertion': client_assertion_jwt
            }
        )
        access_token = resp['body']['access_token']

        # When
        print(f"service_url {service_url}")
        print(f"access_token {access_token}")
        resp = requests.get(f'{service_url}/hello/user', headers={"Authorization": f"Bearer {access_token}"})

        # Then
        assert resp.status_code == 200
        assert 'Hello User' in resp.text
