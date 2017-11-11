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
from google.appengine.ext.webapp import template


class VaultHandler(webapp2.RequestHandler):
    def upload(self):
        file_id = self.request.get("asset_id")
        if self.request.method == 'GET':
            page = utils.template("Vault-upload.html")
            self.response.out.write(template.render(page, {"file_id":file_id}))
            return

        file_content = self.request.get('file')
        vault_entry = Vault().get(file_id=file_id)[0]
        user = User().get(email=vault_entry.email)[0]
        token_url = "https://api.devexhacks.com/oauth2/token?"
        request_params = {
            "client_id": os.environ["co_client_id"],
            "client_secret": os.environ["co_secret"],
            "grant_type": "client_credentials",
        }
        urlencoded_params = urllib.urlencode(request_params)
        token_response = urlfetch.fetch(url=token_url + urlencoded_params, method="POST", deadline=10)
        token_content = json.loads(token_response.content)
        request_header = {
            'Authorization': 'Bearer {}'.format(token_content["access_token"]),
            'Owner-Id': user.owner_id,
            'Content-Type': 'application/octet-stream'
        }
        print token_content["access_token"]
        url = "https://api.devexhacks.com/vault/loading-dock?assetId="+file_id
        response = urlfetch.fetch(
            url=url,
            payload=file_content,
            method="PUT",
            headers=request_header
        )
        print response.status_code
        print response.content
        vault_entry.uploaded = True
        vault_entry.put()
        body_html = """<a href="{}">Access your file here</a>""".format(
            "/".join(self.request.url.split('/')[:-1]) + "/access?asset_id=" + file_id)
        utils.send_mail(
            receiver_email=user.email,
            body=body_html,
            subject="You have a new file in Drop Lock"
        )

    def generate(self):
        auth_code = self.request.get("code")
        file_name = self.request.get("file_name")
        receipient_email = self.request.get("receipient_email")

        user = User().get(code=auth_code)[0]

        token_url = "https://api.devexhacks.com/oauth2/token?"
        request_params = {
            "client_id": os.environ["co_client_id"],
            "client_secret": os.environ["co_secret"],
            "grant_type": "client_credentials",
        }
        urlencoded_params = urllib.urlencode(request_params)
        token_response = urlfetch.fetch(url=token_url + urlencoded_params, method="POST", deadline=10)
        token_content = json.loads(token_response.content)
        request_header = {
            'Authorization': 'Bearer {}'.format(token_content["access_token"]),
        }
        if not user.owner_id:
            address = json.loads(user.address)
            address.update({"streetAddress": address["addressLine1"]})
            del address["addressLine1"]

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

            url = 'https://api.devexhacks.com/vault/owner/match'
            response = urlfetch.fetch(url=url, payload=json.dumps(request_body), method="POST", headers=request_header)

            response_content = json.loads(response.content)
            user.owner_id = response_content["ownerId"]
            user.put()

        url = 'https://api.devexhacks.com/vault/assets'
        request_body = {
            "owners": [{"ownerId": user.owner_id}],
            "assetName": file_name
        }
        response = urlfetch.fetch(
            url=url,
            payload=json.dumps(request_body),
            method="POST",
            headers=request_header
        )
        response_content = json.loads(response.content)
        vault_entry = Vault()
        vault_entry.add(
            email=user.email,
            owner_id=user.owner_id,
            file_id=response_content["assets"][0]["assetId"],
            file_name=file_name,
        )
        print response_content["assets"][0]["assetId"]
        body_html = """<a href="{}">Upload here</a>""".format("/".join(self.request.url.split('/')[:-1])+"/upload?asset_id="+response_content["assets"][0]["assetId"])
        utils.send_mail(
            receiver_email=receipient_email,
            body=body_html,
            subject="{} {} asked you to Upload file to Drop Lock".format(user.first_name.lower().title(), user.last_name.lower().title())
        )

    def access(self):
        file_id = self.request.get("asset_id")

        vault_entry = Vault().get(file_id=file_id)[0]
        user = User().get(email=vault_entry.email)[0]
        token_url = "https://api.devexhacks.com/oauth2/token?"
        request_params = {
            "client_id": os.environ["co_client_id"],
            "client_secret": os.environ["co_secret"],
            "grant_type": "client_credentials",
        }
        urlencoded_params = urllib.urlencode(request_params)
        token_response = urlfetch.fetch(url=token_url + urlencoded_params, method="POST", deadline=10)
        token_content = json.loads(token_response.content)
        request_header = {
            'Authorization': 'Bearer {}'.format(token_content["access_token"]),
            'Owner-Id': user.owner_id,
            'Accept': 'application/json;v=0'
        }
        print request_header
        print token_content["access_token"]
        url = "https://api.devexhacks.com/vault/assets/{}/raw".format(file_id)
        response = urlfetch.fetch(
            url=url,
            method="GET",
            headers=request_header
        )
        self.response.headers['Content-Disposition'] = "attachment; filename={}".format(vault_entry.file_name)
        self.response.headers['Content-Type'] = 'application/octet-stream'
        self.response.out.write(response.content)
