"""
author : pLOPeGG
date : 24/09/2018
abstract : Downloads every podcast from l'Apéro du Captain and store them as mp3 files.

Not widely tested, might fail.
Modify as you want.
"""
import sys
import argparse
import requests
import os
import os.path as path
import re
import itertools


def get_stored_apero(directory):
    rematch_file = re.compile(r'apero_(\d+)\.mp3')
    files = [file for file in os.listdir(directory) if path.isfile(path.join(directory, file))]

    already_stored = []

    for f in files:
        match = rematch_file.match(f)
        if match is not None:
            already_stored += [int(match.group(1))]

    return sorted(already_stored)


def get_remote_apero(n):
    url = f'http://www.captainweb.net/blog/wp-content/uploads/podcast/l-apero-du-captain-{n}.mp3'
    resp = requests.get(url)
    if resp.status_code not in [200]:
        print(f'Apero n°{i} overflew :-( : Error {status}')
    with open(f'docs/apero_{n}.mp3', 'wb') as f:
        f.write(resp.content)
    return resp.status_code


def get_remote_all_apero(directory, lazy=True):
    done = []
    count = 0
    if lazy:
        done = get_stored_apero(directory)
    print(done)
    for i in itertools.count(start=1, step=1):
        if i in done: continue
        print(f'Drinking apéro n°{i} from internet\'s tap...')
        status = get_remote_apero(i)
        if status not in [200]:
            break
        done += [i]
        count += 1
    print(f'Finished !, {count} new apéros drinked')
    print('Your turn to taste these : ')
    print(*done, sep='\n')


def main():
    parser = argparse.ArgumentParser(description='Download all Apéro du captain for you')
    parser.add_argument('too_many_apero', help='don\'t care about this, python on Windows is drunk', default='wtf', nargs='?')
    parser.add_argument('-d', '--directory', help='directory where to store each episode', default='./docs', nargs='?')
    args = parser.parse_args(sys.argv)

    get_remote_all_apero(args.directory)
    pass


if __name__ == '__main__':
    main()
