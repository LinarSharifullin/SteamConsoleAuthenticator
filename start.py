import os
from typing import List

from account import get_accounts, Account
from auto_confirmations_mode import auto_confirmations_router
from accounts_information_mode import accounts_information_router
from confirmations_mode import check_confirmations_router
from exceptions import UserExit
from args_router import args_router


def router(accounts: List[Account]) -> None:
    print(f'\n{len(accounts)} accounts uploaded')
    while True:
        print('\nSteam Console Authenticator 🐭')
        show_menu()
        user_response = input('Write: ')
        if user_response == '0':
            print('\nBye bye')
            return
        try:
            redirect_user(user_response, accounts)
        except TypeError as exc:
            print(f'\n{exc}')
        except UserExit:
            continue


def upload_accounts() -> List[Account]:
    files_from_maFiles = os.listdir('maFiles')
    accounts = get_accounts(files_from_maFiles)
    if len(accounts) == 0:
        raise IndexError('You have no accounts, add maFiles')
    return accounts


def show_menu() -> None:
    print('\nWrite the numeric of the desired mode:')
    print('0. Exit')
    print('1. Work with confirmations')
    print('2. Auto-confirmations')
    print('3. Get 2fa code')
    print('4. Get account information')


def redirect_user(user_response: str, accounts: List[Account]) -> None:
    if user_response == '1':
        check_confirmations_router(accounts)
    elif user_response == '2':
        auto_confirmations_router(accounts)
    elif user_response == '3':
        accounts_information_router(accounts, False)
    elif user_response == '4':
        accounts_information_router(accounts, True)
    else:
        raise TypeError(f'{user_response} not found')


if __name__ == '__main__':
    try:
        accounts = upload_accounts()
    except IndexError as exc:
        print(f'\n{exc}')
        quit()
    try:
        args_router(accounts)
    except TypeError as exc:
        print(exc)
        exit()
    router(accounts)
