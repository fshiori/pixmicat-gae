# -*- coding: utf-8 -*-
from gaeo.controller import BaseController

class WelcomeController(BaseController):
    """The default Controller

    You could change the default route in main.py
    """
    def index(self):
        """The default method

        related to templates/welcome/index.html
        """
        self.redirect('/show/')
