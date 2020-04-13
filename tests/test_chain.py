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
plugin_re_dir = os.path.join(test_dir, "chain_re_plugin")
plugin_info_dir = os.path.join(test_dir, "chain_info_plugin")

tis = []

ti = TInput()
ti.collectors += [gdp.plugin.SubclassPluginCollector(CustomChainPlugin)]
ti.handle += [
    TIO("txt", TxtChainPlugin.answer),
    TIO("json", JsonChainPlugin.answer),
    TIO("yaml", None)
]
ti.descriptions += ["txt", "json"]
ti.id = "Subclass Plugin Collector"
tis.append(ti)

ti = TInput()
ti.collectors += [gdp.plugin.YapsyRegExPluginCollector([plugin_re_dir], "t_plugin_.+.py$")]
ti.handle += [
    TIO("xml", "xml successfully handled"),
    TIO("ini", "ini successfully handled"),
    TIO("yaml", None)
]
ti.descriptions += ["xml", "ini"]
ti.id = "YapsyRegEx Plugin Collector"
tis.append(ti)

ti = TInput()
ti.collectors += [gdp.plugin.YapsyPluginCollector([plugin_info_dir])]
ti.handle += [
    TIO("yaml", "yaml successfully handled"),
    TIO("toml", "toml successfully handled"),
    TIO("txt", None)
]
ti.descriptions += ["yaml", "toml"]
ti.id = "Yapsy Plugin Collector"
tis.append(ti)


ti = TInput()
ti.collectors += [
    gdp.plugin.SubclassPluginCollector(CustomChainPlugin),
    gdp.plugin.YapsyRegExPluginCollector([plugin_re_dir], "t_plugin_.+.py$"),
    gdp.plugin.YapsyPluginCollector([plugin_info_dir])
]
ti.handle += [
    TIO("txt", TxtChainPlugin.answer),
    TIO("json", JsonChainPlugin.answer),
    TIO("xml", "xml successfully handled"),
    TIO("ini", "ini successfully handled"),
    TIO("yaml", "yaml successfully handled"),
    TIO("toml", "toml successfully handled"),
    TIO("noner", None)
]
ti.descriptions += ["txt", "json", "xml", "ini", "yaml", "toml"]
ti.id = "Subclass & YapsyRegEx Plugin Collector & Yapsy Plugin Collector"
tis.append(ti)

ids = [ti.id for ti in tis]


@pytest.mark.parametrize("ti", tis, ids=ids)
def test_handle(ti):
    chain = gdp.chain.build(ti.collectors)

    for io in ti.handle:
        assert chain.handle(io.input) == io.output


@pytest.mark.parametrize("ti", tis, ids=ids)
def test_description(ti):
    chain = gdp.chain.build(ti.collectors)

    assert sorted(chain.description()) == sorted(ti.descriptions)
