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
This package implements items of chain as plugin. Plugin can be class or [Yapsy] plugin. For more information visit [Yapsy documentation] pages.


### How it works in few steps
1. User create chain item (checkers, handlers, descriptions)

2. User set collectors which collect all chain items (plugins)

3. User call build function


### Chain Item Parts
In this implementation, each item of chain is composed of:
* checker - it detects that the request is handleable by the item

* handler - performing unit which processes the request

* description - this part somehow describe the item (it can be string or any other object)

![Chain of plugins design][chain_of_plugins_design]

### Examples
Here is a short minimum example. It implements chain items for pseudo handling different text formats.

![Chain of responsibility example][chain_example]

#### TXT Item
```python
import generic_design_patterns as gdp

class TxtPlugin(gdp.chain.ChainItemPlugin):
    def __init__(self):
        super(TxtPlugin, self).__init__()
        self.checker_class = TxtChecker
        self.handler_class = TxtHandler
        self.description = "txt"

class TxtChecker(gdp.chain.ChainItemPlugin):
    def check(self, input_string):
        return "txt" == input_string.strip()


class TxtHandler(gdp.chain.ChainItemPlugin):
    answer = "txt_handle"

    def handle(self, input_string):
        return self.answer

``` 
#### JSON Item
```python
import generic_design_patterns as gdp

class JsonPlugin(gdp.chain.ChainItemPlugin):
    def __init__(self):
        super(JsonPlugin, self).__init__()
        self.checker_class = JsonChecker
        self.handler_class = JsonHandler
        self.description = "json"


class JsonChecker(gdp.chain.ChainItemPlugin):
    def check(self, input_string):
        return "json" == input_string.strip()


class JsonHandler(gdp.chain.Handler):
    answer = "json_handle"

    def handle(self, input_string):
        return self.answer
``` 

#### Build & Use Chain
```python
import generic_design_patterns as gdp

collectors = [gdp.chain.SubclassPluginCollector(gdp.chain.ChainItemPlugin)]
chain = gdp.chain.build(collectors)

for request in ["txt", "json", "yaml"]:
    result = chain.handle(request)
    print(result)
``` 

```python
>>> txt_handle
>>> json_handle
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
* The subscriber has to implement `update()` method. Package contains `AdvancedSubscriber` class which add methods for subscribe and unsubscribe itself.

* Publisher is created only for this example. Important is line where `notify()` method is called. 

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
print(subscriber.notification)
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
