from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/user',
                  handler=UserHandler,
                  handler_method='user',
                  methods=['GET']),

    webapp2.Route(template='/user/sign_up',
                  handler=UserHandler,
                  handler_method='sign_up',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/user/sign_in',
                  handler=UserHandler,
                  handler_method='sign_in',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/user/dashboard',
                  handler=UserHandler,
                  handler_method='dashboard',
                  methods=['GET']),
])
