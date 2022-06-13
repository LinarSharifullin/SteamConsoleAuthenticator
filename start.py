import os

from account import get_accounts
from auto_confirmations_mode import auto_confirmations_router
from accounts_information_mode import one_time_code_menu
from confirmations_mode import check_confirmations_router


def router() -> None:
    files_from_maFiles = os.listdir('maFiles')
    accounts = get_accounts(files_from_maFiles)
    if len(accounts) == 0:
        print('\nYou have no accounts, add maFiles')
        return
    check_confirmations_router(accounts)
    # one_time_code_menu(accounts)
    # auto_confirmations_router


if __name__ == '__main__':
    router()
