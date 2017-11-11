from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/vault/generate',
                  handler=VaultHandler,
                  handler_method='generate',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/vault/upload',
                  handler=VaultHandler,
                  handler_method='upload',
                  methods=['GET', 'POST']),
])
