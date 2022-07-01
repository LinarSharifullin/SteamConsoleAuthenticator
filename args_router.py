import argparse

from account import check_account_sessions
from auto_confirmations_mode import auto_confirmations
from accounts_information_mode import show_accounts_data
from confirmations_mode import work_with_confirmations
from exceptions import UserExit


def args_router(accounts):
    args = get_args()
    if args.confirmations != None:
        args_confirmations_router(args.confirmations, accounts) 
    elif args.auto_confirmations != None:
        if args.mode == None:
            raise TypeError(f'--mode (-m) not specified')
        args_auto_confirmations_router(args.auto_confirmations, args.mode,
            accounts)
    elif args.information != None:
        args_information_router(args.information, args.full, accounts) 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--confirmations',
        metavar='username',
        help='Return confirmations and a menu for working with them'
    )
    parser.add_argument('-a', '--auto-confirmations',
        nargs='*',
        action='append',
        metavar='list usernames',
        help='Auto-allow the necessary confirmations, selected in --mode (-m)'
    )
    parser.add_argument('-m', '--mode',
        choices=['listings', 'trades', 'both'],
        metavar='{just one thing: listings, trades or both}',
        help='Type confirmations, need for --auto-confirmations (-a)'
    )
    parser.add_argument('-i', '--information',
        nargs='*',
        action='append',
        metavar='list usernames',
        help='Show 2fa codes selected accounts'
    )
    parser.add_argument('-f', '--full', 
        action='store_true',
        help='In addition to the 2fa code, show full information from maFile')
    return parser.parse_args()

def find_accounts_by_usernames(usernames, accounts):
    selected_accounts = []
    for username in usernames:
        found = False
        for account in accounts:
            if username.lower() in account.username.lower():
                selected_accounts.append(account)
                found = True
        if found == False:
            raise TypeError(f'Account {username} not found')
    return list(set(selected_accounts))

def args_confirmations_router(username, accounts):
    selected_accounts = find_accounts_by_usernames([username], accounts)
    check_account_sessions(selected_accounts[0:1], True)
    try:
        work_with_confirmations(selected_accounts[0], True)
    except UserExit:
        quit()
    quit()

def args_auto_confirmations_router(usernames, mode, accounts):
    if len(usernames[0]) == 0:
        selected_accounts = accounts
    else:
        selected_accounts = find_accounts_by_usernames(usernames[0], accounts)
    check_account_sessions(selected_accounts, True)
    listings = False if mode == 'trades' else True
    trades = False if mode == 'listings' else True
    try:
        auto_confirmations(selected_accounts, listings, trades, True)
    except KeyboardInterrupt:
        quit()
    quit()

def args_information_router(usernames, full, accounts):
    if len(usernames[0]) == 0:
        selected_accounts = accounts
    else:
        selected_accounts = find_accounts_by_usernames(usernames[0], accounts)
    show_accounts_data(selected_accounts, full)
    quit()