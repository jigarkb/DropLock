import json
import logging
import traceback
import urllib
import uuid

import webapp2
from google.appengine.api import urlfetch

from .models import Vault
import utils
from User import User
import os


class VaultHandler(webapp2.RequestHandler):
    def generate(self):
        auth_code = self.request.get("code")

        user = User().get(code=auth_code)[0]

    def upload(self):
        auth_code = self.request.get("code")
        user = User().get(code=auth_code)[0]

        if not user.owner_id:
            token_url = "https://api.devexhacks.com/oauth2/token?"
            request_params = {
                "client_id": os.environ["co_client_id"],
                "client_secret": os.environ["co_secret"],
                "grant_type": "client_credentials",
            }
            urlencoded_params = urllib.urlencode(request_params)
            token_response = urlfetch.fetch(url=token_url + urlencoded_params, method="POST", deadline=10)
            token_content = json.loads(token_response.content)

            address = json.loads(user.address)
            address.update({"streetAddress":address["addressLine1"]})
            del address["addressLine1"]

            request_header = {
                'Authorization': 'Bearer {}'.format(token_content["access_token"]),
            }
            print request_header

            request_body = {
                "ownerIdInSourceSystem": user.email,
                "ownerDetails": {
                    "phoneNumber": user.phone,
                    "email": user.email,
                    "dateOfBirth": user.dob,
                    "individual": {
                        "firstName": user.first_name,
                    },
                    "address": address,
                }
            }

            data = urllib.urlencode(request_body)
            url = 'https://api.devexhacks.com/vault/owner/match'
            response = urlfetch.fetch(url=url, payload=json.dumps(request_body), method=urlfetch.POST, headers=request_header)

            response_content = json.loads(response.content)
            user.owner_id = response_content["ownerId"]
            user.put()

