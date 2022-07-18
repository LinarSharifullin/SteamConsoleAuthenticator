from steamcom.guard import generate_one_time_code as get_2fa

from exceptions import UserExit


def accounts_information_router(accounts, full):
    while True:
        show_accounts(accounts)
        user_response = input('Write: ').split()
        try:
            selected_accounts = process_accounts_response(
                user_response, accounts)
        except (TypeError, IndexError) as exc:
            print(f'\n{exc}')
            continue
        show_accounts_data(selected_accounts, full)


def show_accounts(accounts):
    print('\nWrite the numeric of the desired account, '
          'you can several separated by a space:')
    print('0. Return to the main menu')
    print('1. Select all')
    for account_number in range(2, len(accounts)+2):
        print(f'{account_number}. {accounts[account_number-2].username}')


def process_accounts_response(user_response, accounts):
    if '0' in user_response:
        raise UserExit
    elif user_response == []:
        raise TypeError('Empty string received')
    selected_accounts = []
    for part in user_response:
        if part.isnumeric() is False:
            raise TypeError(f'{part} not numeric')
        elif int(part) == 1:
            return accounts
        elif 1 < int(part) <= len(accounts)+1:
            account = accounts[int(part)-2]
            selected_accounts.append(account)
        else:
            raise IndexError(f'{part} not found')
    return selected_accounts


def show_accounts_data(accounts, full=False):
    for account in accounts:
        print(f'\nUsername: {account.username}')
        if full:
            print(f'Password: {account.password}')
            print(f'Shared_secret: {account.shared_secret}')
            print(f'Identity secret: {account.identity_secret}')
        print(f'2fa code: {get_2fa(account.shared_secret)}')
