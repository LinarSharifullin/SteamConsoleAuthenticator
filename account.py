import json
import time

from steamcom.client import SteamClient
from steamcom.exceptions import SessionIsInvalid


class Account:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        account_data = self._read_maFile()
        self.username = account_data['account_name']
        self.password =  account_data['password'] if 'password' \
            in account_data else ''
        self.shared_secret = account_data['shared_secret']
        self.identity_secret = account_data['identity_secret']
        self.session = account_data['Session']
        self.steam_client = SteamClient(self.username, self.password,
            self.shared_secret, self.identity_secret)
        self.save_password = False

    def update_maFile(self) -> None:
        folder = 'maFiles'
        account_data = self._read_maFile()
        self.session = self.steam_client.extract_session()
        account_data['Session'] = self.session
        if self.save_password == True:
            account_data['password'] = self.password
        with open(f'{folder}/{self.file_name}.maFile', 'w') as file:
            json.dump(account_data, file)

    def _read_maFile(self) -> dict:
        folder = 'maFiles'
        with open(f'{folder}/{self.file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)


def get_accounts(files: list[str]) -> list[Account]:
    accounts = []
    for file in files:
        if '.maFile' in file:
            accounts.append(Account(file.replace('.maFile', '')))
    return accounts

def check_account_sessions(accounts: list[Account]) -> None:
    '''Logging in if the session is not valid'''
    delay = 3
    for account in accounts:
        if account.steam_client.was_login_executed == True:
            continue
        try:
            account.steam_client.load_session(account.session)
            print(f'Account {account.username} session restored')
        except SessionIsInvalid:
            if account.password == '':
                ask_for_password(account)
            account.steam_client.login()
            print(f'Signed in account {account.username}')
            account.update_maFile()
        time.sleep(delay)

def ask_for_password(account: Account) -> None:
    account.password = input(f'Enter password for account {account.username}: ')
    account.steam_client.password = account.password
    if account.save_password == False:
        save_password = input('Save password in maFile? Write 1 if yes,'
            'any other character if not: ')
        account.save_password = True if save_password == '1' else False