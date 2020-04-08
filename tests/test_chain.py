import os
import pytest
import generic_design_patterns as gdp


class TestPlugin(gdp.chain.ChainItemPlugin):
    pass


class TxtPlugin(TestPlugin):
    def __init__(self):
        super(TxtPlugin, self).__init__()
        self.checker_class = TxtChecker
        self.handler_class = TxtHandler
        self.description = "txt"


class TxtChecker(gdp.chain.Checker):
    def check(self, input_string):
        return "txt" == input_string.strip()


class TxtHandler(gdp.chain.Handler):
    answer = "txt_handle"

    def handle(self, input_string):
        return self.answer


class JsonPlugin(TestPlugin):
    def __init__(self):
        super(JsonPlugin, self).__init__()
        self.checker_class = JsonChecker
        self.handler_class = JsonHandler
        self.description = "json"


class JsonChecker(gdp.chain.Checker):
    def check(self, input_string):
        return "json" == input_string.strip()


class JsonHandler(gdp.chain.Handler):
    answer = "json_handle"

    def handle(self, input_string):
        return self.answer


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
ti.collectors += [gdp.chain.SubclassPluginCollector(TestPlugin)]
ti.handle += [
    TIO("txt", TxtHandler.answer),
    TIO("json", JsonHandler.answer),
    TIO("yaml", None)
]
ti.descriptions += ["txt", "json"]
ti.id = "Subclass Plugin Collector"
tis.append(ti)

ti = TInput()
ti.collectors += [gdp.chain.YapsyRegExCollector([plugin_dir], "t_plugin_.+.py$")]
ti.handle += [
    TIO("xml", "xml_handle"),
    TIO("ini", "ini_handle"),
    TIO("yaml", None)
]
ti.descriptions += ["xml", "ini"]
ti.id = "YapsyRegEx Plugin Collector"
tis.append(ti)

ti = TInput()
ti.collectors += [
    gdp.chain.SubclassPluginCollector(TestPlugin),
    gdp.chain.YapsyRegExCollector([plugin_dir], "t_plugin_.+.py$")
]
ti.handle += [
    TIO("txt", TxtHandler.answer),
    TIO("json", JsonHandler.answer),
    TIO("xml", "xml_handle"),
    TIO("ini", "ini_handle"),
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
