import os
import json

import steampy


def read_maFile(name):
    with open(f'maFiles/{name}', 'r') as file:
        data = file.read()
    return json.loads(data)

def get_accounts_data(files):
    accounts_data = []
    for file in files:
        if '.maFile' in file:
            accounts_data.append(read_maFile(file))
    return accounts_data

def router():
    files_from_maFiles = os.listdir('maFiles')
    accounts_data = get_accounts_data(files_from_maFiles)

if __name__ == '__main__':
    router()
