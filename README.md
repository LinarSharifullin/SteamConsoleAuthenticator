# Steam Console Authenticator 🐭
<p align="center">
  <img src="https://user-images.githubusercontent.com/48877848/174516452-c8ddebcc-250b-4c9f-afc5-9638c1e7d8a2.png" alt="Steam Console Authenticator main menu">
</p>

Interact with confirmations, get two-factor confirmation codes, get other data from accounts directly from the console. Unfortunately, at the moment it is possible to work only with accounts that already have mafiles, new accounts cannot be installed 🙄

# Installation
1. Install [python](https://python.org), don't forget to check the box in the "Add python to PATH"
2. Download Steam Console Authenticator ([download link](https://github.com/LinarSharifullin/SteamConsoleAuthenticator/archive/refs/heads/main.zip)) and unpack the archive into a convenient directory
3. Open the terminal in the directory with the Steam Console Authenticator and write `pip install -r requirements.txt

# Usage
Just set you maFiles in the `maFiles` folder (⚠️ please use copy of these files, in theory the program may lose them) and run `python start.py` in the terminal in the directory with the Steam Console Authenticator. In `configuration.py` there are settings, you can take a look, I tried to make them very simple and clear

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
the --auto-confirmations flag must necessarily be with --mode. This start auto-confirmations
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
