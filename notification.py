class Notification(object):

    def __init__(self, title, message):
        self.title = title
        self.message = message

        self.source = None
        self.url = None
        self.type = None

        self.date = None

        self.terms = None

        self.length = None

        self.tags = []

        self.sub_type = None

        self.metadata = {}

        self.agent = None

        self.author = None


class NotificationBackend(object):

    def setup(self):
        pass

    def notify(self, notification: Notification):
        pass
