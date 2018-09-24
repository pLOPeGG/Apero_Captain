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
        print(f'Cannot get apero n°{i}, error {status}')
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
        print(f'Drinking apero n°{i} from stream...')
        status = get_remote_apero(i)
        if status not in [200]:
            break
        done += [i]
        count += 1
    print(f'Finished !, Downloaded {count} files')
    print('You can taste all these apero now:')
    print(*done, sep='\n')


def main():
    get_remote_all_apero('./docs')
    pass


if __name__ == '__main__':
    main()
