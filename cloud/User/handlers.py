import json
import logging
import traceback
import uuid

import webapp2

from .models import User
import utils
import os
from google.appengine.ext.webapp import template


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
        code = self.request.get("code", None)
        self.response.out.write("Your code: {}".format(code))

    def sign_in(self):
        code = self.request.get("code", None)
        self.response.out.write("Your code: {}".format(code))


