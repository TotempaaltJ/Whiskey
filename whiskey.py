#!/usr/bin/env python3
from os import path
import re
from datetime import datetime
import json

from namify import namify

TIME_RE = re.compile(r'(?P<day>\d{1,2})-(?P<month>\d{1,2})-(?P<year>\d{4}), '
                     r'(?P<hour>\d{2}):(?P<minute>\d{2})')
PHONE_RE = re.compile(r'(\+[\d ]+\d)')


ACTIONS = ['created', 'added', 'hebt', 'heeft']


class Whiskey(object):
    def __init__(self, root, filename):
        self.root = root
        self.filename = filename
        self.messages = []

    def _namify_match(self, match):
        return namify(match.groups()[0])

    def read(self):
        n = 0
        with open(path.join(self.root, self.filename), 'r') as f:
            for line in f:
                line = line.replace(b"\xe2\x80\xaa".decode(), '')
                line = line.replace(b"\xe2\x80\xac".decode(), '')

                line = re.sub(PHONE_RE, self._namify_match, line)

                msg = {}

                # Parse time
                time = re.match(TIME_RE, line)
                if time is None:
                    self.messages[n-1]['text'] += '\n' + line[:-1]
                    continue

                dt = datetime(
                    int(time.group('year')),
                    int(time.group('month')),
                    int(time.group('day')),
                    int(time.group('hour')),
                    int(time.group('minute'))
                )
                msg['datetime'] = dt.isoformat()
                msg['time'] = line[0:time.end(5)]

                rest = line[time.end(5) + 3:]

                # Find message type
                msg['type'] = 'chat'

                split = rest.find(':')
                for action in ACTIONS:
                    if action in rest and (split == -1 or
                                           rest.find(action) < split):
                        msg['type'] = 'action'
                        msg['author'] = rest[:rest.find(action)].strip()

                        split = rest.find(action)

                if msg['type'] == 'chat':
                    msg['author'] = rest[:split].strip()
                    split += 2

                # Find message
                msg['text'] = rest[split:-1]

                print(msg)
                self.messages.append(msg)

    def write_json(self, outfile):
        with open(outfile, 'w') as f:
            json.dump(self.messages, f, indent=2)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Parse a Whatsapp history file.")
    parser.add_argument('in_file', help="the history file")
    parser.add_argument('out_file', help="a json file to write to")

    args = parser.parse_args()

    glass = Whiskey(*path.split(args.in_file))
    glass.read()
    glass.write_json(args.out_file)
