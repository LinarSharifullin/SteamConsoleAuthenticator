import os
import json
import pickle

from bs4 import BeautifulSoup
from steampy.client import SteamClient, login_required
from steampy.confirmation import ConfirmationExecutor, Confirmation, Tag
from steampy.guard import generate_one_time_code


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

    def get_session(self):
        try:
            self._pickle_load()
            if self._steam_client.is_session_alive() == False:
                raise UserWarning('Session lost')
        except (FileNotFoundError, EOFError, UserWarning):
            self._login()
            self._pickle_dump()
        self._confirmation_executor = ConfirmationExecutor(self._identity_secret,
            self._steam_id, self._steam_client._session)
        self.was_login_executed = True

    def generate_one_time_code(self):
        return generate_one_time_code(self._shared_secret)

    @login_required
    def get_confirmations(self):
        confirmations_page = self._confirmation_executor.\
            _fetch_confirmations_page()
        soup = BeautifulSoup(confirmations_page.text, 'html.parser')
        if soup.select('#mobileconf_empty'):
            return
        return self._parse_confirmations(soup)

    @login_required
    def fetch_confirmation_details_page(self, confirmation):
        return self._confirmation_executor.\
            _fetch_confirmation_details_page(confirmation)

    @login_required
    def send_confirmation_response(self, confirmation, confirm=True):
        tag = Tag.ALLOW if confirm else Tag.CANCEL
        params = self._confirmation_executor._create_confirmation_params(tag.value)
        params['op'] = tag.value,
        params['cid'] = confirmation.data_confid
        params['ck'] = confirmation.data_key
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        return self._steam_client._session.get(self._confirmation_executor.CONF_URL
            + '/ajaxop', params=params, headers=headers).json()

    def _read_maFile(self):
        with open(f'maFiles/{self._file_name}.maFile', 'r') as file:
            data = file.read()
        return json.loads(data)

    def _login(self):
        steam_guard_data = {
            "steamid": self._steam_id,
            "shared_secret": self._shared_secret,
            "identity_secret": self._identity_secret
        }
        self._steam_client = SteamClient('')
        password = self._get_password()
        self._steam_client.login(self._account_name, password, 
            json.dumps(steam_guard_data))
        print(f'Logged into account {self._account_name}')

    def _pickle_dump(self):
        with open(f'maFiles/{self._file_name}.pickle', 'wb') as f:
            pickle.dump(self._steam_client, f)

    def _pickle_load(self):
        with open(f'maFiles/{self._file_name}.pickle', 'rb') as f:
            self._steam_client = pickle.load(f)

    def _get_password(self):
        if self._password == None:
            self._password = input(
                f'Input password for account {self._account_name}: ')
        return self._password

    def _parse_confirmations(self, soup):
        confirmations = []
        for confirmation_div in soup.select\
                ('#mobileconf_list .mobileconf_list_entry'):
            _id = confirmation_div['id']
            data_confid = confirmation_div['data-confid']
            data_key = confirmation_div['data-key']
            confirmation = Confirmation(_id, data_confid, data_key)
            confirmation.text = [elem 
                for elem in confirmation_div.findAll(text=True) 
                if elem != '\n' and elem != ' ']
            confirmation.data_accept = confirmation_div['data-accept']
            confirmations.append(confirmation)
        return confirmations

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
