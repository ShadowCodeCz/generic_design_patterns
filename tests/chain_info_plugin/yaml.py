import generic_design_patterns as gdp


class YamlChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "yaml successfully handled"

    def check(self, input_string):
        return "yaml" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "yaml"
