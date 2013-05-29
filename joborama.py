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
    '/', 'Home',
    '/about', 'About',
)

#-------------------------------------------------------------------------------
app = web.application( urls, globals() )
store = web.session.DiskStore( 'sessions' )
session = web.session.Session( app, store, initializer={'login': 0} )

logg_tmp = web.template.render( 'templates/logged', base="layout" )
anom_tmp = web.template.render( 'templates/anom', base="layout" )

#-------------------------------------------------------------------------------
def logged():
    return (session.login == 1)

#-------------------------------------------------------------------------------
def get_render():
    if logged():
        return logg_tmp
    else:
        return anom_tmp

#-------------------------------------------------------------------------------
class Favicon:
    def GET( self ):
        raise web.seeother('/static/favicon.ico')

#-------------------------------------------------------------------------------
class Home:
    def GET( self ):
        return get_render().main()

#-------------------------------------------------------------------------------
class About:
    def GET( self ):
        return get_render().about()

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()

#-------------------------------------------------------------------------------
