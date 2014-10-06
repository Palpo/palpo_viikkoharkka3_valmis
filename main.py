# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
import logging

import cloudstorage as gcs
from google.appengine.api import app_identity

BUCKET_NAME = os.environ.get('BUCKET_NAME',
                             app_identity.get_default_gcs_bucket_name())

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# http://stackoverflow.com/questions/1916579/in-python-how-can-i-test-if-im-in-google-app-engine-sdk
DEVELOPMENT = os.environ['SERVER_SOFTWARE'].startswith('Development') 


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class AddFileHandler(webapp2.RequestHandler):        
    def post(self):
        name = self.request.get('filename')
        content = self.request.POST['filecontent']
        if name and not isinstance(content, basestring):
            saved = _save_file(name, content.value, content.type)
            if DEVELOPMENT:
                # http://stackoverflow.com/questions/22174903/how-to-serve-cloudstorage-files-using-app-engine-sdk
                added_file_uri = '//' + app_identity.get_default_version_hostname() + '/_ah/gcs' + saved
            else:
                # https://cloud.google.com/storage/docs/reference-uris
                added_file_uri = '//storage.googleapis.com' + saved
        else:
            added_file_uri = None  
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({"added_file_uri": added_file_uri}))
        

def _save_file(name, content, content_type):
    logging.info("Saving %s (size: %i, type: %s)" % (name, len(content), content_type))
    filename = '/' + BUCKET_NAME + '/' + name
    f = gcs.open(filename,
                 'w',
                 content_type=content_type,
                 options={'x-goog-acl': 'public-read'})
    f.write(content)
    f.close()
    return filename

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addfile', AddFileHandler)], debug=True)


