import json
import logging
import traceback
import uuid

import webapp2

from .models import Vault
import utils
import requests
from User import User

class VaultHandler(webapp2.RequestHandler):
    def generate(self):
        pass

    def upload(self):
        user = User.get(email="")
