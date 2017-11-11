import json
import logging
import traceback
import uuid
import pprint
import webapp2

from .models import User
import utils
import os
from google.appengine.ext.webapp import template
import urllib
from google.appengine.api import urlfetch
import time

class UserHandler(webapp2.RequestHandler):
    def user(self):
        sign_up_url = "https://api.devexhacks.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}" \
                      "&scope=signup openid&response_type=code".format(
            client_id=os.environ['co_client_id'],
            redirect_uri="/".join(self.request.url.split('/')[:-1])+"/user/sign_up")

        sign_in_url = "https://api.devexhacks.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}" \
                      "&scope=signin openid&response_type=code".format(
            client_id=os.environ['co_client_id'],
            redirect_uri="/".join(self.request.url.split('/')[:-1])+"/user/sign_in")

        template_variables = {
            "sign_up_url": sign_up_url,
            "sign_in_url": sign_in_url
        }
        page = utils.template("User-login.html")
        self.response.out.write(template.render(page, template_variables))

    def sign_up(self):
        auth_code = self.request.get("code", None)
        token_url = "https://api.devexhacks.com/oauth2/token?"
        request_params = {
            "code": auth_code,
            "client_id": os.environ["co_client_id"],
            "client_secret": os.environ["co_secret"],
            "grant_type": "authorization_code",
            "redirect_uri": "your_redirect_uri",
        }
        urlencoded_params = urllib.urlencode(request_params)
        token_response = urlfetch.fetch(url=token_url+urlencoded_params, method="POST", deadline=10)
        token_content = json.loads(token_response.content)

        userinfo_url = "https://api.devexhacks.com/oauth2/userinfo"
        userinfo_url_headers = {
            "Authorization": "Bearer {access_token}".format(access_token=token_content["access_token"]),
        }
        userinfo_response = urlfetch.fetch(url=userinfo_url, method="GET", deadline=10, headers=userinfo_url_headers)
        userinfo_content = json.loads(userinfo_response.content)["claims"]["identity"][0]["resourceDetails"]
        pprint.pprint(json.loads(userinfo_response.content))
        try:
            user = User()
            user.add(
                email=userinfo_content["email"],
                first_name=userinfo_content["fullName"].split()[0],
                last_name=userinfo_content["fullName"].split()[1],
                dob=userinfo_content["dateOfBirth"],
                phone=userinfo_content["phone"],
                address=json.dumps(userinfo_content["address"]),
                code=auth_code
            )
        except:
            pass
        time.sleep(5)
        self.redirect("/user/dashboard?code={}".format(auth_code))

    def sign_in(self):
        auth_code = "8151af36a0a8478987117a960308bfb2" # self.request.get("code", None)
        self.redirect("/user/dashboard?code={}".format(auth_code))

    def dashboard(self):
        auth_code = self.request.get("code")

        user = User().get(code=auth_code)[0]

        template_variables = {
            "first_name": user.first_name.lower().title(),
            "send_req_url": "/".join(self.request.url.split('/')[:-2])+"/vault/generate?code="+auth_code
                            +"&file_name=myfile.pdf&receipient_email=spencera@usc.edu"
        }
        page = utils.template("User-dashboard.html")
        self.response.out.write(template.render(page, template_variables))
