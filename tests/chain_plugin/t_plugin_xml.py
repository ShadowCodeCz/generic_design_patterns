import generic_design_patterns as gdp


class XMLPlugin(gdp.chain.ChainItemPlugin):
    def __init__(self):
        super(XMLPlugin, self).__init__()
        self.checker_class = XMLChecker
        self.handler_class = XMLHandler
        self.description = "xml"


class XMLChecker(gdp.chain.Checker):
    def check(self, input_string):
        return "xml" == input_string.strip()


class XMLHandler(gdp.chain.Handler):
    answer = "xml_handle"

    def handle(self, input_string):
        return self.answer