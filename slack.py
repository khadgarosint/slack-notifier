import os

import requests

from notification import Notification, NotificationBackend


class Slack(NotificationBackend):

    def __init__(self):
        if not os.environ.get('SLACK_WEBHOOK'):
            raise NotImplemented

        self.webhook = os.environ['SLACK_WEBHOOK']
        self.username = os.environ.get('SLACK_USERNAME')
        self.icon = os.environ.get('SLACK_ICON')
        self.channel = os.environ.get('SLACK_CHANNEL')

    def notify(self, notification: Notification):
        payload = {'text': 'New occurrence detected'}

        if self.username:
            payload['username'] = self.username

        if self.channel:
            payload['channel'] = self.channel

        if self.icon:
            payload['icon_emoji'] = self.icon

        attachment = {'fields': [], 'text': notification.message,
                      'footer': notification.agent}

        if notification.title:
            attachment['title'] = notification.title

        if notification.url:
            attachment['title_link'] = notification.url
            d = {'title': 'URL', 'value': notification.url, 'short': False}
            attachment['fields'].append(d)

        if notification.tags:
            d = {'title': 'Tags', 'value': notification.tags, 'short': False}
            attachment['fields'].append(d)

        if notification.type:
            d = {'title': 'Type', 'value': notification.type, 'short': True}
            attachment['fields'].append(d)

        if notification.sub_type:
            d = {'title': 'Sub Type', 'value': notification.sub_type, 'short': True}
            attachment['fields'].append(d)

        if notification.source:
            d = {'title': 'Source', 'value': notification.source, 'short': True}
            attachment['fields'].append(d)

        if notification.author:
            d = {'title': 'Author', 'value': notification.author, 'short': True}
            attachment['fields'].append(d)

        if notification.terms:
            d = {'title': 'Terms', 'value': ', '.join(notification.terms), 'short': True}
            attachment['fields'].append(d)

        if notification.length:
            d = {'title': 'Length', 'value': notification.length, 'short': True}
            attachment['fields'].append(d)

        for k in notification.metadata.keys():
            if notification.metadata[k]:
                d = {'title': k, 'value': notification.metadata[k], 'short': True}
                attachment['fields'].append(d)

        print(notification.__dict__)

        if notification.date:
            attachment['ts'] = int(notification.date.strftime('%s'))

        payload['attachments'] = [attachment]

        requests.post(self.webhook, json=payload)


backend = Slack
