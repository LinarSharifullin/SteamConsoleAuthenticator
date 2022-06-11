import os

from account import get_accounts
from auto_confirmations_mode import auto_confirmations_router


def router() -> None:
    files_from_maFiles = os.listdir('maFiles')
    accounts = get_accounts(files_from_maFiles)
    auto_confirmations_router(accounts)

if __name__ == '__main__':
    router()
