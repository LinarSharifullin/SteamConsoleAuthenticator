# Steam Console Authenticator 🐭
<sup><b>This program not associated with Valve Corp</b></sup>
<p align="center">
  <img src="https://user-images.githubusercontent.com/48877848/174516452-c8ddebcc-250b-4c9f-afc5-9638c1e7d8a2.png" alt="Steam Console Authenticator main menu">
</p>

Interact with confirmations, get two-factor confirmation codes, get other data from accounts directly from the console. Unfortunately, at the moment it is possible to work only with accounts that already have mafiles, new accounts cannot be installed 🙄

# Installation
1. Install [python](https://python.org), don't forget to check the box in the "Add python to PATH"
2. Download Steam Console Authenticator ([download link](https://github.com/LinarSharifullin/SteamConsoleAuthenticator/archive/refs/heads/main.zip)) and unpack the archive into a convenient directory
3. Open the terminal in the directory with the Steam Console Authenticator and write `pip install -r requirements.txt

# Usage
Just set you maFiles in the `maFiles` folder (⚠️ please use copy of these files, in theory the program may lose them) and run `python start.py` in the terminal in the directory with the Steam Console Authenticator

In `configuration.py` there are settings, you can take a look, I tried to make them very simple and clear

## Flags
With the help of flags, you can skip the main menu and immediately perform the desired action

### --confirmations (-c) username
Calls the menu for working with confirmations
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -c schierke
Account schierke session restored

Write the numberic of the confirmation to be approved, you can specify several, separated by a space, or leave it blank if nothing needs to be confirmed:
0. Exit
1. Select all
2. Confirmation: Sell - Balkan
3. Confirmation: Sell - IDF
4. Confirmation: Sell - Anarchist (Foil)
Write: 
```

You can write only part username, and the command will be executed with the first account, whose username containing this part
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -c schi
Account schierke session restored

Write the numberic of the confirmation to be approved, you can specify several, separated by a space, or leave it blank if nothing needs to be confirmed:
0. Exit
1. Select all
2. Confirmation: Sell - Balkan
3. Confirmation: Sell - IDF
4. Confirmation: Sell - Anarchist (Foil)
Write: 
```

### --auto-confirmations (-a) [list usernames] / --mode (-m) {listings, trades, both}
the `--auto-confirmations` flag must necessarily be with `--mode`. This start auto-confirmations
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -a ken_kaneki schierke -m trades
Account ken_kaneki session restored
Account schierke session restored

Entered auto-confirmation mode, press CTRL + C to exit
No confirmations from account ken_kaneki
Received 3 confirmations from account schierke
No suitable confirmations
```

You can write only parts usernames, and the command will be executed with the accounts, whose usernames contain any of these parts
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -a account -m both
Account account1 session restored
Account account2 session restored
Account account3 session restored

Entered auto-confirmation mode, press CTRL + C to exit
```

If you do not specify any username, the program will launch all accounts
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -a -m listings
Account ken_kaneki session restored
Account account1 session restored
Account account2 session restored
Account account3 session restored
Account schierke session restored

Entered auto-confirmation mode, press CTRL + C to exit
```

### --information (-i) [list usernames] + --full (-f)
If run `-i` without `-f` it show 2fa codes selected accounts
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -i ken_kaneki

Username: ken_kaneki
2fa code: KYV2B
```

If added `-f` it return all information selected accounts
``` console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -i ken_kaneki account1 -f

Username: ken_kaneki
Password: i'm_dead_inside
Shared_secret: QYbzR35CCjL/GG28fdaz=
Identity secret: Zyy8cLG9ZY5cdt4I52uIpVXyc=
2fa code: 54H56

Username: account1
Password: secret_password_for_account1
Shared_secret: !u78zRP5Cpu1au7B28fdaZ=
Identity secret: Hy4hHLq9uYP74boio2TIp3yYc=
2fa code: 4H3C5
```

Just like in the `--auto-confirmations`, it is not necessary to write usernames entirely
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -i ken account1

Username: ken_kaneki
2fa code: Y34P8

Username: account1
2fa code: RGRM3
```

And also you can not specify accounts, in this case all will also start
```console
[linar@fedora SteamConsoleAuthenticator]$ python start.py -i

Username: ken_kaneki
2fa code: YFPV8

Username: account1
2fa code: MC4MC

Username: account2
2fa code: WBMPN

Username: account3
2fa code: 3WYBP

Username: schierke
2fa code: 2HWF5
```
