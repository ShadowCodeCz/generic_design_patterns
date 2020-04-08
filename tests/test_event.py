import pytest
import generic_design_patterns as gdp


class TestSubscriber(gdp.event.Subscriber):
    def __init__(self):
        self.notification = None

    def update(self, notification):
        self.notification = notification


class AdvancedTestSubscriber(gdp.event.AdvancedSubscriber):
    def __init__(self, provider):
        self.notification = None
        super(AdvancedTestSubscriber, self).__init__(provider)

    def update(self, notification):
        self.notification = notification


class Message(object):
    test_message = "test_message"
    test_message_2 = "test_message_2"


@pytest.fixture()
def provider():
    return gdp.event.Provider()


@pytest.fixture()
def subscriber_1():
    return TestSubscriber()


@pytest.fixture()
def subscriber_2():
    return TestSubscriber()


@pytest.fixture()
def notification_1():
    return gdp.event.Notification(Message.test_message)


@pytest.fixture()
def notification_2():
    return gdp.event.Notification(Message.test_message_2)


def test_subscribe(provider, subscriber_1):
    provider.subscribe(Message.test_message, subscriber_1)
    assert subscriber_1 in provider.subscription[Message.test_message]


def test_unsubscribe(provider, subscriber_1):
    provider.subscribe(Message.test_message, subscriber_1)
    provider.unsubscribe(Message.test_message, subscriber_1)
    assert subscriber_1 not in provider.subscription[Message.test_message]


def test_notify(provider, subscriber_1, notification_1):
    provider.subscribe(notification_1.message, subscriber_1)
    provider.notify(notification_1)
    assert notification_1.message == subscriber_1.notification.message


def test_notify_more_subscribers(provider, subscriber_1, subscriber_2, notification_1):
    provider.subscribe(notification_1.message, subscriber_1)
    provider.subscribe(notification_1.message, subscriber_2)
    provider.notify(notification_1)
    assert notification_1.message == subscriber_1.notification.message
    assert notification_1.message == subscriber_2.notification.message


def test_notify_by_queue(provider, subscriber_1, notification_1, notification_2):
    provider.subscribe(notification_1.message, subscriber_1)
    provider.subscribe(notification_2.message, subscriber_1)
    q = [notification_1, notification_2]
    provider.notify_by_queue(q)
    assert notification_2.message == subscriber_1.notification.message


def test_advanced_subscriber(provider, notification_1):
    subscriber = AdvancedTestSubscriber(provider)
    subscriber.subscribe(notification_1.message)
    assert subscriber in provider.subscription[notification_1.message]
    provider.notify(notification_1)
    assert notification_1.message == subscriber.notification.message
    subscriber.unsubscribe(notification_1.message)
    assert subscriber not in provider.subscription[notification_1.message]