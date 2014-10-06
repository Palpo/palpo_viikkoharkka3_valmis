# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class AddFileHandler(webapp2.RequestHandler):        
    def post(self):
        name = self.request.get('filename')
        content = self.request.POST['filecontent']
        if name and not isinstance(content, basestring):
            data = content.value
            content_type = content.type
            
            logging.info("Saving %s (size: %i, content type: %s" % (name, len(data), content_type))
            
            # TODO: tallenna cloud storageen

            added_file_uri = "//example.com/foo/bar"
            
            
        else:
            added_file_uri = None

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({"added_file_uri": added_file_uri}))
        


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addfile', AddFileHandler)], debug=True)


