import generic_design_patterns as gdp


class TomlChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "toml successfully handled"

    def check(self, input_string):
        return "toml" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "toml"
