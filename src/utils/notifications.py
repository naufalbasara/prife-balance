from mac_notifications import client

class Notifications:
    def __init__(self, os):
        self.__os = os

    def notify(self, message):
        client.create_notification(
        title='Testing',
        subtitle='Hello world!'
        )