import os
import json


from configuration import *


class Account:
    def __init__(self, file_name: str) -> None:
        self._file_name = file_name
        account_data = self._read_maFile()
        self.username = ['account_name']
        self.password =  account_data['password'] if 'password' \
            in account_data else None
        self.shared_secret = account_data['shared_secret']
        self.identity_secret = account_data['identity_secret']

    def _read_maFile(self) -> dict:
        folder = 'maFiles'
        with open(f'{folder}/{self._file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)


def get_accounts(files: list[str]) -> list[Account]:
    accounts = []
    for file in files:
        if '.maFile' in file:
            accounts.append(Account(file.strip('.maFile')))
    return accounts

def router() -> None:
    files_from_maFiles = os.listdir('maFiles')
    # accounts = get_accounts(files_from_maFiles)

if __name__ == '__main__':
    router()