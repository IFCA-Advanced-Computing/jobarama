#!/bin/env python

#-------------------------------------------------------------------------------
import web
from web.wsgiserver import CherryPyWSGIServer

#-------------------------------------------------------------------------------
CherryPyWSGIServer.ssl_certificate = "cert/server.crt"
CherryPyWSGIServer.ssl_private_key = "cert/server.key"

web.config.debug = False

#-------------------------------------------------------------------------------
urls = (
    '/favicon.ico', 'Favicon',
    '/', 'home',
)

#-------------------------------------------------------------------------------
app = web.application( urls, globals() )

#-------------------------------------------------------------------------------
class Favicon:
    def GET( self ):
        raise web.seeother('/static/favicon.ico')

#-------------------------------------------------------------------------------
class home:
    def GET( self ):
        return "GET main"

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()

#-------------------------------------------------------------------------------
