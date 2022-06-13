import time
from typing import Tuple, List

from steamcom.models import Confirmation, ConfirmationType

from account import Account, check_account_sessions


def auto_confirmations_router(accounts: List[Account]) -> None:
    selected_accounts = []
    while True:
        if len(selected_accounts) == 0:
            show_accounts(accounts)
            user_response = input('Write: ').split()
            if '0' in user_response:
                return
            elif user_response == []:
                print('\nEmpty string received')
                continue
            try:
                selected_accounts = process_accounts_response(user_response,
                    accounts)
            except (TypeError, IndexError) as exc:
                print(f'\n{exc}')
                continue
            check_account_sessions(selected_accounts)

        show_confirmations_mode()
        user_response = input('Write: ')
        if user_response == '0':
            return
        try:
            listings, trades = process_confirmations_mode_response(
                user_response)
        except TypeError as exc:
            print(f'\n{exc}')
            continue

        if listings == True or trades == True:
            try:
                auto_confirmations(selected_accounts, listings, trades)
            except KeyboardInterrupt:
                return

def show_accounts(accounts: List[Account]) -> None:
    print('\nWrite the numeric of the desired account, '
        'you can several separated by a space:')
    print('0. Return to the main menu')
    print('1. Select all')
    for account_number in range(2, len(accounts)+2):
        print(f'{account_number}. {accounts[account_number-2].username}')

def process_accounts_response(user_response: List[str],
        accounts: List[Account]) -> List[Account]:
    selected_accounts = []
    for part in user_response:
        if part.isnumeric() == False:
            raise TypeError(f'{part} not numeric')
        elif int(part) == 1:
            return accounts
        elif 1 < int(part) <= len(accounts)+1:
            account = accounts[int(part)-2]
            selected_accounts.append(account)
        else:
            raise IndexError(f'{part} not found')
    return selected_accounts

def show_confirmations_mode() -> None:
    print('\nWrite the numeric of the desired confirmations:')
    print('0. Return to the main menu')
    print('1. Market transactions')
    print('2. Trades')
    print('3. Both (market transactions and trades)')

def process_confirmations_mode_response(user_response: str) -> Tuple[bool]:
    listings, trades = False, False
    if '3' == user_response:
        listings, trades = True, True
    elif '1' == user_response:
        listings = True
    elif '2' == user_response:
        trades = True
    else:
        raise TypeError(f'{user_response} not found')
    return listings, trades

def auto_confirmations(accounts: List[Account], listings: bool,
        trades: bool) -> None:
    print('\nEntered auto-confirmation mode, press CTRL + C',
        'to exit in main menu')
    delay = 30
    while True:
        for account in accounts:
            try:
                confirmations = account.steam_client.confirmations\
                    .get_confirmations()
                if len(confirmations) > 0:
                    process_confirmations(confirmations, listings,
                        trades, account)
                else:
                    print(f'No confirmations from account {account.username}')
            except (AttributeError, IndexError) as exc:
                print('An error occurred while receiving',
                    f'confirmations: {exc}')
            time.sleep(delay)

def process_confirmations(confirmations: List[Confirmation], listings: bool,
        trades: bool, account: Account) -> None:
    print(f'Received {len(confirmations)} confirmations from', 
        f'account {account.username}')
    confirmations_for_allow = []
    create_listing_value = ConfirmationType.create_listing.value
    trades_value = ConfirmationType.trade.value
    for confirmation in confirmations:
        conf_type = confirmation.conf_type
        if listings == True and create_listing_value == conf_type:
            confirmations_for_allow.append(confirmation)
        if trades == True and trades_value == conf_type:
            confirmations_for_allow.append(confirmation)
    if len(confirmations_for_allow) <= 0:
        print('No suitable confirmations')
        return
    status = account.steam_client.confirmations\
                .respond_to_confirmations(confirmations_for_allow)
    if status == True:
        print(f'Approved {len(confirmations_for_allow)}',
            'confirmations')
    else:
        print('An error occurred while approving',
            f'{len(confirmations_for_allow)} confirmations')