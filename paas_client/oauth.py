import jwt
import requests
import uuid
from oauthlib.oauth2 import LegacyApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
from time import time

# Dependent on environment
def _redirect_uri(base): return f"{base}/callback"
def _auth_url(base): return f"{base}/auth/realms/api-producers/protocol/openid-connect/auth"
def _access_token_url(base): return f"{base}/auth/realms/api-producers/protocol/openid-connect/token"
def _aud_url(base): return f"{base}/auth/realms/api-producers"
SCOPE = ["openid"]

"""Return a token and client upon successful login

The function requires the client_id and base_auth_url
To authenticate, provide either the following:
- The client_secret, username and get_password (user account login)
- The private_key (machine user login)
- The token

Parameters:
client_id (string): 
base_auth_url (string): URL of the authentication server eg "https://identity.ptl.api.platform.nhs.uk"
client_secret (string?)
username (string?)
private_key (string?): Full path of the private key file eg "/home/test/client.key"
get_password (function?): A callback for the client password eg "lambda: 'password'"
token (string?): The same token that is returned by this function, can be used for refresh workflow

Returns:
token (Dict): Contains access and refresh token
client (session): Authenticated HTTP client session
"""
def get_authenticated_client_token(*, client_id, base_auth_url, client_secret=None, username=None, private_key=None, get_password=None, token=None):
  def token_saver(_token):
    token = _token
  if token and token["expires_at"] >= time() + 5:
    # Try refresh token login flow first
    try:
      oauth = OAuth2Session(client_id, token=token, auto_refresh_url=_access_token_url(base_auth_url),
        scope=SCOPE, token_updater=token_saver)
    except TokenExpiredError:
      pass
    else:
      return oauth.token, oauth
  if username and get_password:
    # User login flow
    client = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
    token = client.fetch_token(token_url=_access_token_url(base_auth_url),
      username=username, password=get_password(), client_id=client_id,
      client_secret=client_secret)
  elif private_key:
    # Machine user login flow
    claims = {
      "sub": client_id,
      "iss": client_id,
      "jti": str(uuid.uuid4()),
      "aud": _aud_url(base_auth_url),
      "exp": int(time()) + 300,
    }
    # with open(private_key, "r") as f:
    #   private_key = f.read()
    client_assertion = jwt.encode(claims, private_key, algorithm="RS512")
    token_response = requests.post(
      _access_token_url(base_auth_url),
      data={
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assertion,
      },
    )

    assert token_response.status_code == 200
    client = requests.session()
    client.headers.update({"Authorization": f"Bearer {token_response.json()['access_token']}"})
    token = token_response.json()
    token["expires_in"] = int(time()) + 300
  else:
    raise RuntimeError("Must provide username and fetch password or private key")
  return token, client
