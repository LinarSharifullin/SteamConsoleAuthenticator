import time

from requests.exceptions import InvalidSchema
from steamcom.models import ConfirmationType

from account import check_account_sessions, account_login_router
from accounts_information_mode import show_accounts, process_accounts_response
from exceptions import UserExit
from configuration import (
    delay_between_check_confirmations, delay_before_allow_confirmations)


def auto_confirmations_router(accounts):
    while True:
        selected_accounts = select_accounts(accounts)
        listings, trades = select_confirmation_mode()

        try:
            auto_confirmations(selected_accounts, listings, trades)
        except KeyboardInterrupt:
            return


def select_accounts(accounts):
    while True:
        show_accounts(accounts)
        user_response = input('Write: ').split()
        try:
            selected_accounts = process_accounts_response(
                user_response, accounts)
        except (TypeError, IndexError) as exc:
            print(f'\n{exc}')
            continue
        try:
            check_account_sessions(selected_accounts)
        except UserExit:
            continue
        return selected_accounts


def select_confirmation_mode():
    while True:
        show_confirmations_mode()
        user_response = input('Write: ')
        try:
            listings, trades = process_confirmations_mode_response(
                user_response)
        except TypeError as exc:
            print(f'\n{exc}')
            continue
        return listings, trades


def show_confirmations_mode():
    print('\nWrite the numeric of the desired confirmations:')
    print('0. Return to the main menu')
    print('1. Market transactions (listings)')
    print('2. Trades')
    print('3. Both (market transactions and trades)')


def process_confirmations_mode_response(user_response):
    listings, trades = False, False
    if user_response == '0':
        raise UserExit
    elif '1' == user_response:
        listings = True
    elif '2' == user_response:
        trades = True
    elif '3' == user_response:
        listings, trades = True, True
    else:
        raise TypeError(f'{user_response} not found')
    return listings, trades


def auto_confirmations(accounts, listings, trades, flag_mode=False):
    exit_text = 'to exit in main menu' if flag_mode is False else 'to exit'
    print('\nEntered auto-confirmation mode, press CTRL + C', exit_text)
    while True:
        for account in accounts:
            try:
                confirmations = account.steam_client.confirmations\
                    .get_confirmations()
                if len(confirmations) > 0:
                    time.sleep(delay_before_allow_confirmations)
                    process_confirmations(
                        confirmations, listings, trades, account)
                else:
                    print(f'No confirmations from account {account.username}')
            except (AttributeError, IndexError) as exc:
                print('An error occurred while receiving',
                      f'confirmations: {type(exc).__name__}: {exc.args[0]}')
            except InvalidSchema:
                print(f'Account {account.username} lost connection,',
                      'log in again...')
                account.steam_client.was_login_executed = False
                try:
                    account_login_router(account, flag_mode)
                except UserExit:
                    return
            time.sleep(delay_between_check_confirmations)


def process_confirmations(confirmations, listings, trades, account):
    print(f'Received {len(confirmations)} confirmations from',
          f'account {account.username}')
    confirmations_for_allow = []
    for confirmation in confirmations:
        conf_type = confirmation.type
        if listings and ConfirmationType.CREATE_LISTING == conf_type:
            confirmations_for_allow.append(confirmation)
        if trades and ConfirmationType.TRADE == conf_type:
            confirmations_for_allow.append(confirmation)
    if len(confirmations_for_allow) <= 0:
        print('No suitable confirmations')
        return
    status = account.steam_client.confirmations\
        .respond_to_confirmations(confirmations_for_allow)
    if status:
        print(f'Approved {len(confirmations_for_allow)}',
              'confirmations')
    else:
        print('An error occurred while approving',
              f'{len(confirmations_for_allow)} confirmations')
