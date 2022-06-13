from typing import List

from steamcom.models import Confirmation

from account import Account, check_account_sessions


def check_confirmations_router(accounts: List[Account]) -> None:
    while True:
        if len(accounts) == 0:
            print('\nYou have no accounts, add maFiles')
            return
        show_accounts(accounts)
        user_response = input('Write: ')
        if user_response == '0':
            return
        try:
            account = process_account_response(user_response, accounts)
        except (TypeError, IndexError) as exc:
            print(f'\n{exc}')
            continue
        check_account_sessions([account])

        confirmations = show_confirmations(account)
        if len(confirmations) == 0:
            continue
        user_response = input('Write: ').split()
        if '0' in user_response:
            return
        elif user_response == []:
            continue
        try:
            selected_confirmations = process_confirmations_response(
                user_response,confirmations)
        except (TypeError, IndexError) as exc:
            print(f'\n{exc}')
            continue
        if len(selected_confirmations) > 0:
            allow_confirmations(account, selected_confirmations)


def show_accounts(accounts: List[Account]) -> None:
        print('\nWrite the numeric of the desired account:')
        print('0. Return to the main menu')
        for account_number in range(1, len(accounts)+1):
            print(f'{account_number}. {accounts[account_number-1].username}')

def process_account_response(user_response: str,
        accounts: List[Account]) -> Account:
    if user_response.isnumeric() == False:
        raise TypeError(f'{user_response} not numeric')
    elif 0 < int(user_response) <= len(accounts):
        account = accounts[int(user_response)-1]
        return account
    else:
        raise IndexError(f'{user_response} not found')

def show_confirmations(account: Account) -> List[Confirmation]:
    confirmations = account.steam_client.confirmations.get_confirmations()
    if len(confirmations) == 0:
        print('\nYou have no confirmations')
        return []
    print('\nWrite the numberic of the confirmation to be approved,',
        'you can specify several, separated by a space,',
        'or leave it blank if nothing needs to be confirmed:')
    print('0. Return to the main menu')
    print('1. Select all')
    for conf_number in range(2, len(confirmations)+2):
        print(f'{conf_number}. {confirmations[conf_number-2]}')
    return confirmations

def process_confirmations_response(user_response: list,
        confirmations: List[Confirmation]) -> List[Confirmation]:
    selected_confirmations = []
    for part in user_response:
        if part.isnumeric() == False:
            raise TypeError(f'{part} not numeric')
        elif int(part) == 1:
            return confirmations
        elif 1 < int(part) <= len(confirmations)+1:
            confirmation = confirmations[int(part)-2]
            selected_confirmations.append(confirmation)
        else:
            raise IndexError(f'{part} not found')
    return selected_confirmations

def allow_confirmations(account: Account,
        confirmations: List[Confirmation]) -> None:
    status = account.steam_client.confirmations\
        .respond_to_confirmations(confirmations)
    if status == True:
        print(f'\nApproved {len(confirmations)}',
            'confirmations')
    else:
        print('\nAn error occurred while approving',
            f'{len(confirmations)} confirmations')