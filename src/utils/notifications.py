from mac_notifications import client

class Notifications:
    def __init__(self, os: str = 'mac'):
        self.__os = os

    def notify(self, notification_type: str, title:str, subtitle:str, message: str):
        client.create_notification(
        title=title,
        subtitle=subtitle,
        text=message
        )