import os
import json

from steamcom.guard import generate_one_time_code as get_2fa


class Account:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        account_data = self._read_maFile()
        self.username = account_data['account_name']
        self.password =  account_data['password'] if 'password' \
            in account_data else None
        self.shared_secret = account_data['shared_secret']
        self.identity_secret = account_data['identity_secret']

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
        print('Write the numeric of the desired account, '
            'you can several separated by a space:')
        print('0. To return to the main menu')
        if len(accounts) == 0:
            print('You have no accounts, add maFiles')
        else:
            for account_number in range(1, len(accounts)):
                print(f'{account_number}. {accounts[account_number].username}')
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
        elif 0 < int(part) <= len(accounts)-1:
            account = accounts[int(part)]
            print(f'{account.username}: {get_2fa(account.shared_secret)}')
        else:
            print(f'{part} not found')
    print()
    return exit

def router() -> None:
    files_from_maFiles = os.listdir('maFiles')
    accounts = get_accounts(files_from_maFiles)
    one_time_code_menu(accounts)

if __name__ == '__main__':
    router()