import time
from typing import Tuple, List

from account import Account, check_account_sessions


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
                return

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
    if user_response == []:
        print('Empty string received')
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
    print()
    print('Entered auto-confirmation mode, press CTRL + C to exit in main menu')
    delay = 30
    while True:
        try:
            for account in accounts:
                try:
                    confirmations = account.steam_client.confirmations\
                        .get_confirmations()
                except AttributeError:
                    print('An error occurred while receiving',
                        'confirmations: AttributeError')
                except IndexError:
                    print('An error occurred while receiving',
                        'confirmations: IndexError')
                if len(confirmations) == 0:
                    print(f'No confirmations from account {account.username}')
                    time.sleep(delay)
                    continue
                confirmations_for_allow = []
                print(f'Received {len(confirmations)} confirmations from', 
                    f'account {account.username}')
                for confirmation in confirmations:
                    if sellings == True\
                            and confirmation.data_accept == 'Create Listing':
                        confirmations_for_allow.append(confirmation)
                    elif trades == True\
                            and confirmation.data_accept == 'Send Offer':
                        confirmations_for_allow.append(confirmation)
                if len(confirmations_for_allow) <= 0:
                    print('No suitable confirmations')
                    continue
                status = account.steam_client.confirmations\
                            .respond_to_confirmations(confirmations_for_allow)
                if status == True:
                    print(f'Approved {len(confirmations_for_allow)}', 
                        'confirmations')
                else:
                    print('An error occurred while approving',
                        f'{len(confirmations_for_allow)} confirmations')
                time.sleep(delay)
        except KeyboardInterrupt:
            return