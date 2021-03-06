#!/usr/bin/env python3

from datetime import datetime
import yaml
import argparse
import os
import sys
import subprocess
from journal import journal



def response(question):
    answer = input('[?] {}: [y/n] '.format(question))
    if not answer or answer[0].lower() != 'y':
        return False
    return True


def main():
    with open('config.yaml') as f:
        config = yaml.load(f)

    home = os.path.expanduser('~')
    datadir = os.path.join(home, '.journalist')

    parser = argparse.ArgumentParser()
    parser.add_argument('task', help='Task to do', type=str, choices=['write', 'view'])
    parser.add_argument('name', help='The name of the journal', type=str)

    args = parser.parse_args()
    name = args.name

    journal_path = os.path.join(datadir, name)
    if not os.path.exists(journal_path):
        print('[!] The journal {} does not exist!'.format(name))
        res = response('Do you want to create journal {}'.format(name))
        if res:
            os.makedirs(journal_path)
        else:
            sys.exit()

    if args.task=='write':
        date = datetime.now()
        filename = date.strftime('%Y-%m-%d-%a') + '.md'
        curdir = os.path.join(datadir, name, date.strftime('%Y'), date.strftime('%m'))
        if not os.path.exists(curdir):
            os.makedirs(curdir)

        filepath = os.path.join(curdir, filename)
        subprocess.call([config['Global']['Editor'], filepath])
    else:
        print('[*] Starting Journalist viewer webapp...')
        print('[*] View this journal at http://127.0.0.1:5000/journalist?name={}'.format(name))
        journal.app.run()


if __name__=='__main__':
    main()
