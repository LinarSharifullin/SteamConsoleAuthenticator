import json
import time

from steamcom.client import SteamClient
from steamcom.exceptions import SessionIsInvalid, LoginFailed

from exceptions import UserExit
from configuration import delay_between_check_account_sessions, save_password


class Account:
    def __init__(self, file_name):
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
        self.save_password = True if save_password == 'yes' else False
        self.ask_about_password_saving = True if save_password == 'ask'\
            else False

    def update_maFile(self):
        account_data = self._read_maFile()
        self.session = self.steam_client.extract_session()
        account_data['Session'] = self.session
        if self.save_password == True:
            account_data['password'] = self.password
        with open(f'maFiles/{self.file_name}.maFile', 'w') as file:
            json.dump(account_data, file)

    def _read_maFile(self) -> dict:
        with open(f'maFiles/{self.file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)


def get_accounts(files):
    accounts = []
    for file in files:
        if '.maFile' in file:
            accounts.append(Account(file.replace('.maFile', '')))
    return accounts

def check_account_sessions(accounts, flag_mode=False):
    '''Logging in if the session is not valid'''
    for account in accounts:
        if account.steam_client.was_login_executed == True:
            continue
        try:
            account.steam_client.load_session(account.session)
            print(f'Account {account.username} session restored')
        except SessionIsInvalid:
            print(f'Saved session account {account.username} is invalid,',
                'we login again...')
            account_login(account, flag_mode)
        if accounts[-1] != account:
            time.sleep(delay_between_check_account_sessions)

def account_login(account, flag_mode=False):
    while True:
        if account.password == '':
            ask_for_password(account)
        try:
            account.steam_client.login()
            print(f'Logged into the {account.username} account')
            account.update_maFile()
            print(f'Updated maFile from account {account.username}')
            return
        except LoginFailed as exc:
            login_error_handling(account, exc, flag_mode)
            
def login_error_handling(account, exc, flag_mode=False):
    while True:
        print(f'\nAn error occurred during login in {account.username}: {exc}')
        exit_text = 'Back to account selection' if flag_mode == False else 'Exit'
        print('0.', exit_text)
        print('1. Try again')
        print('2. Change password')
        user_response = input('Write: ')
        if user_response == '0':
            if flag_mode:
                exit('\nBye bye')
            raise UserExit
        elif user_response == '1':
            return
        elif user_response == '2':
            account.password = ''
            return
        else:
            print(f'\n{user_response} not found')

def ask_for_password(account):
    account.password = input(f'Enter password for account {account.username}: ')
    account.steam_client.password = account.password
    if account.ask_about_password_saving == True:
        save_password = input('Save password in maFile? Write 1 if yes,'
            'any other character if not: ')
        account.save_password = True if save_password == '1' else False