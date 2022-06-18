import argparse
import os
from typing import List

from account import get_accounts, Account
from auto_confirmations_mode import auto_confirmations_router
from accounts_information_mode import accounts_information_router
from confirmations_mode import check_confirmations_router
from exceptions import UserExit


def args_router(accounts: List[Account]) -> None:
    args = get_args()

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--confirmations',
        metavar='username',
        help='Return confirmations and a menu for working with them'
    )
    parser.add_argument('-a', '--auto-confirmations',
        nargs='*',
        action='append',
        metavar='list usernames',
        help='Auto-allow the necessary confirmations, selected in --mode (-m)'
    )
    parser.add_argument('-m', '--mode',
        choices=['listings', 'trades', 'both'],
        metavar='just one thing: listings, trades or both',
        help='Type confirmations, need for --auto-confirmations (-a)'
    )
    parser.add_argument('-i', '--information',
        nargs='*',
        action='append',
        metavar='list usernames',
        help='Show 2fa codes selected accounts'
    )
    parser.add_argument('-f', '--full', 
        action='store_true',
        help='In addition to the 2fa code, show full information from maFile')
    return parser.parse_args()

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
    args_router(accounts)
    router(accounts)