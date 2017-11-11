import json
import logging
import traceback
import uuid

import webapp2

from .models import Vault
import utils


class VaultHandler(webapp2.RequestHandler):
    def generate(self):
        pass

    def upload(self):
        pass
