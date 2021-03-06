from handlers.base import BaseHandler


class SimpleTemplateHandler(BaseHandler):
    """
    Renders a simple template directly.
    Let js do the rest rendering.
    """
    template = ""

    def initialize(self, template=""):
        self.template = template

    def get(self):
        args = self.request.arguments
        self.render(self.template, query_string=args)
