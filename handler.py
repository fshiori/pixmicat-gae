# -*- coding: utf-8 -*-
import webapp2
from webapp2_extras import jinja2
from webapp2_extras import i18n

class BaseHandler(webapp2.RequestHandler):
    
    def __init__(self, request, response):
        # Set self.request, self.response and self.app.
        self.initialize(request, response)
        # ... add your custom initializations here ...
        lang = self.app.config.get('PIXMICAT_LANGUAGE') 
        i18n.get_i18n().set_locale(lang) # sample locale assigned               

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
        
    def render_template(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        return rv
    
    def render_error(self, message, _template='error.html'):
        context = {'message' : message}
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)        