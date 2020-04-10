import os
import pytest
import generic_design_patterns as gdp


class CustomChainPlugin(gdp.chain.ChainNodePlugin):
    pass


class TxtChainPlugin(CustomChainPlugin):
    answer = "txt successfully handled"

    def check(self, input_string):
        return "txt" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "txt"


class JsonChainPlugin(CustomChainPlugin):
    answer = "json successfully handled"

    def check(self, input_string):
        return "json" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "json"


class TInput:
    def __init__(self):
        self.collectors = []
        self.handle = []
        self.descriptions = []
        self.id = ""


class TIO:
    def __init__(self, i, o):
        self.input = i
        self.output = o


test_dir = os.path.dirname(os.path.abspath(__file__))
plugin_dir = os.path.join(test_dir, "chain_plugin")

tis = []

ti = TInput()
ti.collectors += [gdp.chain.SubclassPluginCollector(CustomChainPlugin)]
ti.handle += [
    TIO("txt", TxtChainPlugin.answer),
    TIO("json", JsonChainPlugin.answer),
    TIO("yaml", None)
]
ti.descriptions += ["txt", "json"]
ti.id = "Subclass Plugin Collector"
tis.append(ti)

ti = TInput()
ti.collectors += [gdp.chain.YapsyRegExCollector([plugin_dir], "t_plugin_.+.py$")]
ti.handle += [
    TIO("xml", "xml successfully handled"),
    TIO("ini", "ini successfully handled"),
    TIO("yaml", None)
]
ti.descriptions += ["xml", "ini"]
ti.id = "YapsyRegEx Plugin Collector"
tis.append(ti)

ti = TInput()
ti.collectors += [
    gdp.chain.SubclassPluginCollector(CustomChainPlugin),
    gdp.chain.YapsyRegExCollector([plugin_dir], "t_plugin_.+.py$")
]
ti.handle += [
    TIO("txt", TxtChainPlugin.answer),
    TIO("json", JsonChainPlugin.answer),
    TIO("xml", "xml successfully handled"),
    TIO("ini", "ini successfully handled"),
    TIO("yaml", None)
]
ti.descriptions += ["txt", "json", "xml", "ini"]
ti.id = "Subclass & YapsyRegEx Plugin Collector"
tis.append(ti)

ids = [ti.id for ti in tis]


@pytest.mark.parametrize("ti", tis, ids=ids)
def test_handle(ti):
    chain = gdp.chain.build(ti.collectors)

    for io in ti.handle:
        assert chain.handle(io.input) == io.output


@pytest.mark.parametrize("ti", tis, ids=ids)
def test_descriptions(ti):
    chain = gdp.chain.build(ti.collectors)

    assert sorted(chain.descriptions()) == sorted(ti.descriptions)
