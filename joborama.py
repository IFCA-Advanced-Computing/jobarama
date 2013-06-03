#!/bin/env python

#-------------------------------------------------------------------------------
import web
from web.wsgiserver import CherryPyWSGIServer
import os.path
import sys
import json
import database
import data
import pipeline

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
    '/logout', 'Logout',
    '/ajax/file', 'AjaxFiles',
    '/ajax/job', 'AjaxJobs',
    '/job/(.*)', 'Job',
    '/file/(.*)', 'File',
)

#-------------------------------------------------------------------------------
app = web.application( urls, globals() )
store = web.session.DiskStore( 'sessions' )
session = web.session.Session( app, store, initializer={'login': 0, 'user': None} )

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
def clearSession():
    session.login = 0
    session.user = None

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
            if database.checkUser( name, passwd ):
                session.login = 1
                session.user = name
            else:
                clearSession()
        except:
            clearSession()

        if logged():
            raise web.seeother('/')
        else:
            raise web.seeother('/login_error')

#-------------------------------------------------------------------------------
class LoginError:
    def GET( self ):
        return get_render().login_error()

#-------------------------------------------------------------------------------
class Logout:
    def GET( self ):
        session.login = 0
        session.kill()
        raise web.seeother('/')

#-------------------------------------------------------------------------------
class AjaxFiles:
    def GET( self ):
        if logged():
            web.header('Content-Type', 'application/json')
            files = database.getUserFiles( session.user )
            return json.dumps( {'files': files} )
        else:
            raise web.seeother('/')

    def PUT( self ):
        if logged():
            x = web.input(myfile={})

            try:
                filename = data.getUserFilename( session.user, x['myfile'].filename )
                data.saveFile( filename, x['myfile'].file )
                database.insertFile( session.user, x['myfile'].filename )
            except:
                print sys.exc_info()
                web.debug( "can't save file" )

            return "OK"

        else:
            raise web.seeother('/')

#-------------------------------------------------------------------------------
class AjaxJobs:
    def GET( self ):
        if logged():
            web.header('Content-Type', 'application/json')
            jobs = database.getUserJobs( session.user )
            return json.dumps( {'jobs': jobs} )
        else:
            raise web.seeother('/')

    def POST( self ):
        if logged():
            x = web.input()
            try:
                pipeline.startJob( session.user, x.var1, int(x.file) )
            except:
                print sys.exc_info()
                web.debug( "can't start new job" )

            return "OK"
        else:
            raise web.seeother('/')

#-------------------------------------------------------------------------------
class File:
    def GET( self, fileid ):
        if logged():
            if database.isFileAllowedFromUser( fileid, session.user ):
                return "get file " + str(fileid)
            else:
                return get_render().notallowed()
        else:
            raise web.seeother('/')

#-------------------------------------------------------------------------------
class Job:
    def GET( self, jobid ):
        if logged():
            if database.isJobFromUser( jobid, session.user ):
                jobinfo = database.getJobInfo( jobid )
                return get_render().job( jobinfo )
            else:
                return get_render().notallowed()
        else:
            raise web.seeother('/')

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    database.init()
    p = pipeline.run()
    app.run()
    p.terminate()

#-------------------------------------------------------------------------------
