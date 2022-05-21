import os
import json
import pickle

from steampy.client import SteamClient
from steampy.confirmation import ConfirmationExecutor


class Account:
    def __init__(self, file_name):
        self._file_name = file_name
        account_data = self._read_maFile()
        self._shared_secret = account_data['shared_secret']
        self._account_name = account_data['account_name']
        self._identity_secret = account_data['identity_secret']
        self._steam_id = str(account_data['Session']['SteamID'])
        self._password =  account_data['password'] if 'password' \
            in account_data else None
        self._get_session()

    def _read_maFile(self):
        with open(f'maFiles/{self._file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)

    def _get_session(self):
        try:
            self._pickle_load()
            if self._steam_client.is_session_alive() == False:
                raise UserWarning('Session lost')
        except (FileNotFoundError, EOFError, UserWarning):
            self._login()
            self._pickle_dump()
        self._confirmation_executor = ConfirmationExecutor(self._identity_secret,
            self._steam_id, self._steam_client._session)

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

    def _pickle_dump(self):
        with open(f'maFiles/{self._file_name}.pickle', 'wb') as f:
            pickle.dump(self._steam_client, f)

    def _pickle_load(self):
        with open(f'maFiles/{self._file_name}.pickle', 'rb') as f:
            self._steam_client = pickle.load(f)

    def _get_password(self):
        if self._password == None:
            self._password = input(
                f'Input password for account {self._account_name}: ')
        return self._password

    def get_confirmations(self):
        return self._confirmation_executor._get_confirmations()

    def fetch_confirmation_details_page(self, confirmation):
        return self._confirmation_executor.\
            _fetch_confirmation_details_page(confirmation)

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
