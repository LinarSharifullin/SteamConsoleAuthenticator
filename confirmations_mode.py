from account import check_account_sessions
from exceptions import UserExit


def check_confirmations_router(accounts):
    while True:
        account = select_account(accounts)
        work_with_confirmations(account)

def select_account(accounts):
    while True:
        show_accounts(accounts)
        user_response = input('Write: ')
        try:
            account = process_account_response(user_response, accounts)
        except (TypeError, IndexError) as exc:
            print(f'\n{exc}')
            continue
        try:
            check_account_sessions([account])
        except UserExit:
            continue
        return account

def work_with_confirmations(account, flag_mode=False):
    while True:
        confirmations = show_confirmations(account, flag_mode)
        if len(confirmations) == 0:
            return
        user_response = input('Write: ').split()
        try:
            selected_confirmations = process_confirmations_response(
                user_response,confirmations)
        except (TypeError, IndexError) as exc:
            print(f'\n{exc}')
            continue
        if len(selected_confirmations) > 0:
            allow_confirmations(account, selected_confirmations)
        return

def show_accounts(accounts):
        print('\nWrite the numeric of the desired account:')
        print('0. Return to the main menu')
        for account_number in range(1, len(accounts)+1):
            print(f'{account_number}. {accounts[account_number-1].username}')

def process_account_response(user_response, accounts):
    if user_response == '0':
        raise UserExit
    if user_response.isnumeric() == False:
        raise TypeError(f'{user_response} not numeric')
    elif 0 < int(user_response) <= len(accounts):
        account = accounts[int(user_response)-1]
        return account
    else:
        raise IndexError(f'{user_response} not found')

def show_confirmations(account, flag_mode):
    confirmations = account.steam_client.confirmations.get_confirmations()
    if len(confirmations) == 0:
        print(f'\nNo confirmations from account {account.username}')
        return []
    print('\nWrite the numberic of the confirmation to be approved,',
        'you can specify several, separated by a space,',
        'or leave it blank if nothing needs to be confirmed:')
    exit_text = '0. Return to the main menu' if flag_mode == False else '0. Exit'
    print(exit_text)
    print('1. Select all')
    for conf_number in range(2, len(confirmations)+2):
        print(f'{conf_number}. {confirmations[conf_number-2]}')
    return confirmations

def process_confirmations_response(user_response, confirmations):
    if '0' in user_response:
        raise UserExit
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

def allow_confirmations(account, confirmations):
    status = account.steam_client.confirmations\
        .respond_to_confirmations(confirmations)
    if status == True:
        print(f'\nApproved {len(confirmations)}',
            'confirmations')
    else:
        print('\nAn error occurred while approving',
            f'{len(confirmations)} confirmations')