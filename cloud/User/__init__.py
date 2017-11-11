from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/user/sign_up',
                  handler=UserHandler,
                  handler_method='sign_up',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/user/sign_in',
                  handler=UserHandler,
                  handler_method='sign_in',
                  methods=['GET', 'POST']),
])