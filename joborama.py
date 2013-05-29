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
    '/login', 'Login',
    '/login_error', 'LoginError',
)

#-------------------------------------------------------------------------------
app = web.application( urls, globals() )
store = web.session.DiskStore( 'sessions' )
session = web.session.Session( app, store, initializer={'login': 0} )

#-------------------------------------------------------------------------------
def logged():
    return (session.login == 1)

#-------------------------------------------------------------------------------
def get_render():
    if logged():
        return web.template.render( 'templates/logged', base="layout" )
    else:
        return web.template.render( 'templates/anom', base="layout" )

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
class Login:
    def GET( self ):
        raise web.seeother('/')

    def POST(self):
        try:
            name = web.input().user
            passwd = web.input().passwd
            if name == "admin" and passwd == "aa":
                session.login = 1
            else:
                session.login = 0
        except:
            session.login = 0

        if logged():
            raise web.seeother('/')
        else:
            raise web.seeother('/login_error')

#-------------------------------------------------------------------------------
class LoginError:
    def GET( self ):
        return get_render().login_error()

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()

#-------------------------------------------------------------------------------
