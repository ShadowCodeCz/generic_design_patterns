import datetime
import yapsy.PluginFileLocator
import yapsy.PluginManager
import yapsy.IPlugin


class PluginCollector(object):
    def collect(self):
        raise NotImplemented


class YapsyPluginCollector(PluginCollector):
    def __init__(self, plugin_directories, plugin_locator=None):
        self.plugin_manager = yapsy.PluginManager.PluginManager(directories_list=plugin_directories,
                                                                plugin_locator=plugin_locator)

    def collect(self):
        plugins = []
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugins.append(plugin.plugin_object)
        return plugins


class YapsyRegExCollector(YapsyPluginCollector):
    def __init__(self, plugin_directories, regexp):
        locator = yapsy.PluginFileLocator.PluginFileLocator()
        locator.setAnalyzers([yapsy.PluginFileLocator.PluginFileAnalyzerMathingRegex(self._analyzer_name(), regexp)])
        super(YapsyRegExCollector, self).__init__(plugin_directories, locator)

    def _analyzer_name(self):
        return "YapsyPluginReAnalyzer%s" % datetime.datetime.now()


class SubclassPluginCollector(PluginCollector):
    def __init__(self, base_class):
        self.base_class = base_class

    def collect(self):
        plugins = []
        for subclass_plugin in self.base_class.__subclasses__():
            plugins.append(subclass_plugin())
        return plugins


def build(collectors):
    return Builder.build(collectors)


class Builder(object):
    @staticmethod
    def build(collectors):
        plugins = Builder.collect(collectors)
        chain = ChainItem(None, EndChainItem())
        chain = Builder.add_plugins_to_chain(chain, plugins)
        return chain

    @staticmethod
    def collect(collectors):
        plugins = []
        for collector in collectors:
            plugins += collector.collect()
        return plugins

    @staticmethod
    def add_plugins_to_chain(chain, plugins):
        for plugin in plugins:
            chain = ChainItem(chain, plugin)
        return chain


class ChainItem(object):
    def __init__(self, successor, plugin):
        self.successor = successor
        self.checker = plugin.checker_class()
        self.handler = plugin.handler_class()
        self.description = plugin.description

    def handle(self, *args, **kwargs):
        if self.checker.check(*args, **kwargs):
            return self.handler.handle(*args, **kwargs)
        else:
            if self.successor:
                return self.successor.handle(*args, **kwargs)

    def descriptions(self):
        if self.successor is None:
            return []
        else:
            descriptions = self.successor.descriptions()
            descriptions.append(self.description)
            return descriptions


class ChainItemPlugin(yapsy.IPlugin.IPlugin):
    def __init__(self):
        super(ChainItemPlugin, self).__init__()
        self.checker_class = None
        self.handler_class = None
        self.description = None


class Checker(object):
    def check(self, *args, **kwargs):
        raise NotImplemented


class Handler(object):
    def handle(self, *args, **kwargs):
        raise NotImplemented


class AlwaysTrueChecker(Checker):
    def check(self, *args, **kwargs):
        return True


class EndHandler(Handler):
    def handle(self, *args, **kwargs):
        return None


class EndChainItem(object):
    def __init__(self):
        self.checker_class = AlwaysTrueChecker
        self.handler_class = EndHandler
        self.description = None

