import generic_design_patterns as gdp


class XmlChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "xml successfully handled"

    def check(self, input_string):
        return "xml" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "xml"