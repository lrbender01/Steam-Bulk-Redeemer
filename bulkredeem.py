#!/usr/bin/env python3

# Bulk Steam key redeemer written with ValvePython's steam library for
# interacting with Steam servers.
#
# Takes text file with line separated keys.
#
# Written by Luke Bender (lrbender01@gmail.com) on 6-1-21

# https://steam.readthedocs.io/en/latest/index.html
# https://github.com/ValvePython/steam

import steam.webauth as wa
from getpass import getpass
import json
import sys

def main():
    # Get username and password
    username = input('Username: ')
    password = getpass('Password: ')
    user = wa.WebAuth(username, password)

    try: # Try to login
        user.login()
    except wa.LoginIncorrect: # Wrong password
        print('Incorrect password\nExiting...')
        sys.exit(1)
    except wa.CaptchaRequired: # Captcha required
        user_code = input(f'Input code from this captcha: {user.captcha_url}\nCode: ')
        user.login(captcha = user_code)
    except wa.EmailCodeRequired: # Email code required
        user_code = input(f'Input code from two-factor authentication email\nCode: ')
        user.login(email_code = user_code)
    except wa.TwoFactorCodeRequired: # Steam Guard code required
        user_code = input(f'Input code from Steam Guard on your phone\nCode: ')
        user.login(twofactor_code = user_code)

    # List of key strings
    keys = []

    # Get input file
    file_path = input('Input file: ')

    # Try to open file
    try:
        file = open(file_path)
    except:
        print(f'\'{file_path}\' cannot be opened\nExiting...')
        sys.exit(1)
    
    # Parse file into keys removing whitespace
    for key in file:
        keys.append(key.strip())
    file.close()

    # Get sessionid for posting key requests
    user_session_id = user.session.cookies.get_dict()['sessionid']

    for key in keys:
        # Post key request with user session
        response = user.session.post('https://store.steampowered.com/account/ajaxregisterkey/',
                                    data = {'product_key' : key, 'sessionid' : user_session_id})
        response_blob = json.loads(response.text)

        # Check success
        if response_blob['success'] == 1:
            for item in response_blob['purchase_receipt_info']['line_items']:
                title = item['line_item_description']
                print(f'[{key}] [SUCCESS] {title}')
        else:
            # Error codes from: https://steamstore-a.akamaihd.net/public/javascript/registerkey.js?l=english
            error_code = response_blob['purchase_result_details']

            # Take care of all possible error codes
            if error_code == 9: # Duplicate ownership
                for item in response_blob['purchase_receipt_info']['line_items']:
                    title = item['line_item_description']
                    print(f'[{key}] [ERROR] {username} already owns this product ({title})')

            elif error_code == 13: # Key unavailable in country
                print(f'[{key}] [ERROR] This product isn\'t available in your country')

            elif error_code == 14: # Key invalid
                print(f'[{key}] [ERROR] This product key isn\'t valid')

            elif error_code == 15: # Key already activated
                print(f'[{key}] [ERROR] This product key has already been activated')

            elif error_code == 24: # Key requires base-game
                print(f'[{key}] [ERROR] This product requires ownership of another product before\
                    it can be redeemed')

            elif error_code == 36: # Key requires playing on PS3
                print(f'[{key}] [ERROR] This product requires that you first play the game on PS3\
                    before redeeming')

            elif error_code == 50: # Key isn't a game key
                print(f'[{key}] [ERROR] This product key is a Steam Gift Card or Steam Wallet Code\
                    and can\'t be redeemed here')

            elif error_code == 53: # Account is on cooldown (I think this happens at 48 keys in an hour)
                print(f'[{key}] [ERROR] This account ({username}) or IP address has been issuing\
                    too many recent activation requests')

            else: # Some unknown issue
                print(f'[{key}] [ERROR] Some unknown error has occurred. Try again later or contact\
                    Steam Support here: https://help.steampowered.com/en/wizard/HelpWithCDKey')

# Always call main()
if __name__ == '__main__':
    main()