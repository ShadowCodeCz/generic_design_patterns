# Generic Design Patterns
Python package implements design patterns in generic way. Its can be used in a wide range of projects.
Some of these patterns are slightly improved for efficient use in real-world projects.

## Installation 
```python
pip install generic-design-patterns 
``` 

## Implemented Patterns
* Chain of responsibility 

* Event Provider

* Specification


## Chain Of Responsibility
The purpose of this text is not to explain the principles of CoR. For example, source describing CoR is [refactoring.guru].
This package implements node of chain as plugin. Plugin can be average class or [Yapsy] plugin. For more information visit [Yapsy documentation] pages.


### How it works in few steps
1. User create chain node plugin

2. User set collectors which collect all chain nodes (plugins)

3. User call build function


### Chain Node
Chain node have to inherit from  `gdp.chain.ChainNodePlugin`, which inherit form `yapsy.IPlugin.IPlugin`. 

Each node of chain have to implement these methods:
* `check()` - It detects that the request is handleable by the node. The method has to return bool value.

* `handle()` - It is performing method which processes the request. It returns result. 

* `description()` - It returns string or any other class which describes the node/plugin.

All nodes/plugins (in one chain) have to implement `check()` and `handle()` with same arguments.    

### Examples
Here is a short minimum example. It implements chain nodes for pseudo handling different text formats.

![Chain of responsibility example][chain_example]

#### TXT Node Plugin
```python
import generic_design_patterns as gdp

class TxtChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "txt successfully handled"

    def check(self, input_string):
        return "txt" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "txt"
``` 

#### JSON Node Plugin
```python
import generic_design_patterns as gdp

class JsonChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "json successfully handled"

    def check(self, input_string):
        return "json" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "json"
``` 

#### Build & Use Chain
```python
import generic_design_patterns as gdp

collectors = [gdp.chain.SubclassPluginCollector(gdp.chain.ChainNodePlugin)]
chain = gdp.chain.build(collectors)

for request in ["txt", "json", "yaml"]:
    result = chain.handle(request)
    print(result)
``` 

```python
>>> txt successfully handled
>>> json successfully handled
>>> None
``` 

#### Plugin Collectors

## Event Provider
This standard implementation of publisher-subscriber design pattern. There are not any improvements. Note that current implementation is only for single thread/process usage. 

### How it works
* Main part is event provider, which store subscriptions. On the basis of subscriptions provider directs notifications to right subscribers. 

* Subscribers can register at provider.

* Publishers can send notification via provider.

### Examples
The code shows minimum example. Note:
* The subscriber has to implement `update()` method. The package contains `AdvancedSubscriber` class which add methods for subscribe and unsubscribe itself.

* The publisher is created only for this example. Important is line where `notify()` method is called. 

* The example shows how to make subscription. It has to part string `message` and `subscriber` object.

* Use notification class from this package or your custom class which should inherit from it. The most import is that notification has to contain message attribute.

```python
import generic_design_patterns as gdp

dummy_message = "dummy message"

class DummySubscriber(gdp.event.Subscriber):
    def __init__(self):
        self.notification = None

    def update(self, notification):
        print(notification.message)

class DummyPublisher:
    def __init__(self, provider):
        self.provider = provider
    
    def publish(self):
        dummy_notification = gdp.event.Notification(dummy_message)
        self.provider.notify(dummy_notification)

provider = gdp.event.Provider()

subscriber = DummySubscriber()
provider.subscribe(dummy_message, subscriber)

publisher = DummyPublisher(provider)
publisher.publish()

print(subscriber.notification.message)
``` 

```python
>>> dummy message
``` 

## Specification



[chain_example]: img/chain_example.svg "Chain of responsibility example"
[chain_of_plugins_design]: img/chain_plugin_design.svg "Chain of plugins design"
[refactoring.guru]: https://refactoring.guru/design-patterns/chain-of-responsibility
[Yapsy]: https://pypi.org/project/Yapsy/
[Yapsy documentation]: http://yapsy.sourceforge.net/
