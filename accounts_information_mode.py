from steamcom.guard import generate_one_time_code as get_2fa

from account import Account


def one_time_code_menu(accounts: list[Account]) -> None:
    exit = False
    while exit != True:
        print()
        print('Write the numeric of the desired account, '
            'you can several separated by a space:')
        print('0. Return to the main menu')
        for account_number in range(1, len(accounts)+1):
            print(f'{account_number}. {accounts[account_number-1].username}')
        user_response = input('Write: ').split()
        exit = one_time_code_user_response_processing(user_response, accounts)

def one_time_code_user_response_processing(user_response: list[str], 
        accounts: list[Account]) -> bool:
    exit = False
    print()
    if user_response == []:
        print('Empty string received')
    for part in user_response:
        if part.isnumeric() == False:
            print(f'{part} not numeric')
        elif int(part) == 0:
            exit = True
        elif 0 < int(part) <= len(accounts):
            account = accounts[int(part)-1]
            print(f'{account.username}: {get_2fa(account.shared_secret)}')
        else:
            print(f'{part} not found')
    return exit