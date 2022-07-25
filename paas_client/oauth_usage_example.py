#!/usr/bin/env python

"""
oauth_usage_example.py

example of sucessfully accessing a auth URL via Proxygen 

Usage:
  oauth_usage_example.py <private_key> <client_id>  
  oauth_usage_example.py (-h | --help)

Options:
  -h --help                        Show this screen.  
  <private_key>                    Private key
  <client_id>                      Client ID
"""

import requests
import oauth
from docopt import docopt

def authenticate_with_machine_user(private_key, client_id):
  # Authenticate with private key (machine user)
  token, client = oauth.get_authenticated_client_token(
    client_id=client_id,
    base_auth_url='https://identity.ptl.api.platform.nhs.uk',
    # private_key='/path/to/private.key'
    private_key=private_key)
  
  return token, client

def authenticate_with_user_account():
  # Authenticate with username and password (user)
  token, client = oauth.get_authenticated_client_token(
    client_id='paas-test-client',
    client_secret='',
    base_auth_url='https://identity.ptl.api.platform.nhs.uk',
    username='',
    get_password=lambda: 'password')

  return token, client

def main(args):
  private_key = args['<private_key>']
  client_id = args['<client_id>']

  token, client = authenticate_with_machine_user(private_key,client_id)

  # Choose method of authentication
  # token, client = authenticate_with_user_account()

  # Test with authenticated client
  response_using_client = client.get('https://proxygen.ptl.api.platform.nhs.uk/apis/hello-paas')
  print(response_using_client)

  # Test with token directly
  response_using_token = requests.get(
    'https://proxygen.ptl.api.platform.nhs.uk/apis/hello-paas', 
    headers={"Authorization": f"Bearer {token['access_token']}"})
  print(response_using_token)


if __name__ == "__main__":
  main(docopt(__doc__, version='1'))
