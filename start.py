import os
import json
import time
from typing import Tuple, List

from steamcom.guard import generate_one_time_code as get_2fa
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
            accounts.append(Account(file.strip('.maFile')))
    return accounts

def one_time_code_menu(accounts: list[Account]) -> None:
    exit = False
    while exit != True:
        print()
        print('Write the numeric of the desired account, '
            'you can several separated by a space:')
        print('0. To return to the main menu')
        if len(accounts) == 0:
            print('You have no accounts, add maFiles')
        else:
            for account_number in range(1, len(accounts)+1):
                print(f'{account_number}. {accounts[account_number-1].username}')
        user_response = input('Write: ').split()
        exit = one_time_code_user_response_processing(user_response, accounts)

def one_time_code_user_response_processing(user_response: list[str], 
        accounts: list[Account]) -> bool:
    exit = False
    print()
    for part in user_response:
        if part.isnumeric() == False:
            print(f'{part} not numeric')
        elif int(part) == 0:
            exit = True
        elif 0 < int(part) <= len(accounts):
            account = accounts[int(part)-1]
            print(f'{account.username}: {get_2fa(account.shared_secret)}')
        else:
            print(f'{part} not found')
    return exit

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

def auto_confirmations_router(accounts: list[Account]) -> None:
    exit = False
    selected_accounts = []
    while exit == False:
        if len(selected_accounts) == 0:
            selected_accounts, exit = select_accounts(accounts)
        else:
            check_account_sessions(selected_accounts)
            exit, sellings, trades = select_auto_confirmations_mode()
            if exit == False and sellings == True or trades == True:
                auto_confirmations(selected_accounts, sellings, trades)

def select_accounts(accounts: list[Account]) -> List[Account]:
    print()
    print('Write the numeric of the desired account, '
        'you can several separated by a space:')
    print('0. Return to the main menu')
    print('1. To select all')
    if len(accounts) == 0:
        print('You have no accounts, add maFiles')
    else:
        for account_number in range(1, len(accounts)+1):
            print(f'{account_number+1}. {accounts[account_number-1].username}')
        user_response = input('Write: ').split()
        selected_accounts, exit = select_accounts_user_response_processing(
            user_response, accounts)
    return selected_accounts, exit

def select_accounts_user_response_processing(user_response: list[str], 
        accounts: list[Account]) -> Tuple[list[Account], bool]:
    exit = False
    selected_accounts = []
    for part in user_response:
        if part.isnumeric() == False:
            print(f'{part} not numeric')
            return [], False
        elif int(part) == 0:
            return [], True
        elif int(part) == 1:
            return accounts, False
        elif 1 < int(part) <= len(accounts)+1:
            account = accounts[int(part)-2]
            selected_accounts.append(account)
        else:
            print(f'{part} not found')
            return [], False
    return selected_accounts, exit

def select_auto_confirmations_mode() -> Tuple[bool]:
    exit, sellings, trades = False, False, False
    print()
    print('Write the numeric of the desired confirmations:')
    print('0. Return to the main menu')
    print('1. Market transactions')
    print('2. Trades')
    print('3. Both (market transactions and trades)')
    user_response = input('Write: ')
    if '0' == user_response:
        exit = True
    elif '3' == user_response:
        sellings, trades = True, True
    elif '1' == user_response:
        sellings = True
    elif '2' == user_response:
        trades = True
    else:
        print(f'{user_response} - invalid response')
    return exit, sellings, trades

def auto_confirmations(accounts: list[Account], sellings: bool,
        trades: bool) -> None:
    print([i.username for i in accounts], sellings, trades)

def router() -> None:
    files_from_maFiles = os.listdir('maFiles')
    accounts = get_accounts(files_from_maFiles)
    one_time_code_menu(accounts)

if __name__ == '__main__':
    router()