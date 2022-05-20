import os
import json

from steampy.client import SteamClient


class Account:
    def __init__(self, file_name):
        self._file_name = file_name
        account_data = self._read_maFile()
        self._shared_secret = account_data['shared_secret']
        self._account_name = account_data['account_name']
        self._identity_secret = account_data['identity_secret']
        self._steam_id = account_data['Session']['SteamID']
        self._password =  account_data['password'] if 'password' \
            in account_data else None
        self._login()
    
    def _read_maFile(self):
        with open(f'maFiles/{self._file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)
    
    def _login(self):
        steam_guard_data = {
            "steamid": self._steam_id,
            "shared_secret": self._shared_secret,
            "identity_secret": self._identity_secret
        }
        self._steam_client = SteamClient('')
        password = self._get_password()
        self._steam_client.login(self._account_name, password, 
            json.dumps(steam_guard_data))
        print(f'Logged into account {self._account_name}')
    
    def _get_password(self):
        if self._password == None:
            self._password = input(
                f'Input password for account {self._account_name}: ')
        return self._password


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
