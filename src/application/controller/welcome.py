from gaeo.controller import BaseController

class WelcomeController(BaseController):
    """The default Controller

    You could change the default route in main.py
    """
    def index(self):
        """The default method

        related to templates/welcome/index.html
        """
        import datetime
        import tz_helper
        import settings
        tz = tz_helper.timezone(settings.TIME_ZONE)
        now = datetime.datetime.now(tz)
        #self.render(text='Exception: %s' % now)
