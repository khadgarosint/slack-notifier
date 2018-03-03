import os

import rethinkdb as r
from dateutil.parser import parse as dtparse

from notification import Notification
from slack import Slack
from datetime import datetime
import traceback

notifiers = []

if __name__ == '__main__':

    try:
        slack = Slack()
        notifiers.append(slack)
    except Exception as e:
        print('[-] Failed to initialize Slack: {}'.format(str(e)))

    r.connect(os.environ.get('RETHINK_HOST', 'localhost'), int(os.environ.get('RETHINK_PORT', 28015))).repl()

    cursor = r.db('khadgar').table('url').changes().run()
    for document in cursor:
        try:
            print(document)
            if 'new_val' in document and not document['old_val']:
                d = document['new_val']
                n = Notification(d['title'], d['summary'])
                n.length = d['length']
                n.url = d['url']
                n.source = d['source']
                n.author = d['author']
                n.terms = d['terms']
                n.type = d['type']
                n.sub_type = d['sub_type']
                n.metadata = d['metadata']
                try:
                    n.date = dtparse(d['date'])
                except:
                    n.date = datetime.now()
                n.tags = d['tags']
                n.agent = d['agent']

                for b in notifiers:
                    b.notify(n)
        except:
            traceback.print_exc()
            continue
