import os


class Account:
    def __init__(self, file_name, need_session=True):
        self._file_name = file_name
        account_data = self._read_maFile()
        self._shared_secret = account_data['shared_secret']
        self._account_name = account_data['account_name']
        self._identity_secret = account_data['identity_secret']
        self._steam_id = str(account_data['Session']['SteamID'])
        self._password =  account_data['password'] if 'password' \
            in account_data else None
        self.was_login_executed = False
        if need_session == True:
            self.get_session()

def get_accounts(files):
    accounts = []
    for file in files:
        if '.maFile' in file:
            accounts.append(Account(file.strip('.maFile')))
    return accounts

def router():
    files_from_maFiles = os.listdir('maFiles')
    # accounts = get_accounts(files_from_maFiles)

if __name__ == '__main__':
    router()