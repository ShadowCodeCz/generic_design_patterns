import generic_design_patterns as gdp


class IniChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "ini successfully handled"

    def check(self, input_string):
        return "ini" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "ini"

