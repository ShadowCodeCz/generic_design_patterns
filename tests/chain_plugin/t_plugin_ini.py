import generic_design_patterns as gdp


class IniPlugin(gdp.chain.ChainItemPlugin):
    def __init__(self):
        super(IniPlugin, self).__init__()
        self.checker_class = InIChecker
        self.handler_class = InIHandler
        self.description = "ini"


class InIChecker(gdp.chain.Checker):
    def check(self, input_string):
        return "ini" == input_string.strip()


class InIHandler(gdp.chain.Handler):
    answer = "ini_handle"

    def handle(self, input_string):
        return self.answer