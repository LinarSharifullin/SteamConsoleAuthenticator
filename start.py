import os
import json

import steampy


class Account:
    def __init__(self, file_name):
        self._file_name = file_name
        account_data = self._read_maFile()
        self._shared_secret = account_data['shared_secret']
        self._account_name = account_data['account_name']
        self._identity_secret = account_data['identity_secret']
        self._steam_id = account_data['Session']['SteamID']
    
    def _read_maFile(self):
        with open(f'maFiles/{self._file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)


def get_accounts(files):
    accounts = []
    for file in files:
        if '.maFile' in file:
            accounts.append(Account(file.strip('.maFile')))
    return accounts

def router():
    files_from_maFiles = os.listdir('maFiles')
    accounts = get_accounts(files_from_maFiles)

if __name__ == '__main__':
    router()
