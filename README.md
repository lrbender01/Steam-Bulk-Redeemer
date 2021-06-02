# Steam Bulk Redeemer

### bulkredeem.py
This script can be used to redeem Steam product keys in bulk from any text file with line-separated product keys. It uses [ValvePython](https://github.com/ValvePython)'s excellent [steam](https://github.com/ValvePython/steam) package to interact with and authenticate on Valve's servers.

I wrote this script to be as readable as possible as I did not want to trust any other bulk key redeemer with my login information. I know this assumes that ValvePython is honest but after some scrutiny of their source code and a thorough look through their documentation I thought that it was worth trusting with my credentials.

Feel free to reach out to me with any problems you encounter while using this script to redeem keys of your own. I have linked my more technical sources in bulkredeem.py itself.

### keys.txt
This is an example input file with some dummy keys that have already been redeemed. Replace them with your own unless you want product activation to fail.

### Dependencies
The only libraries that bulkredeem.py uses are [getpass](https://docs.python.org/3/library/getpass.html), [json](https://docs.python.org/3/library/json.html), [sys](https://docs.python.org/3/library/sys.html), and [steam](https://github.com/ValvePython/steam). View [steam's documentation](https://steam.readthedocs.io/en/latest/index.html) for detailed information on installation. I was able to install it and all its dependencies with pip as shown below:
```
pip install -U steam[client]
```

### Usage
Just run bulkredeem.py with your Python 3.4+ installation or alone if your Python environment variable is set up correctly. Provide all of the input it asks for. I do not have a lot of input checking in place right now so I cannot promise that incorrect input won't cause a runtime error.

### Other Information
I wrote this script primarily to help me quickly redeem a backlog of Humble Choice / Humble Monthly keys that I had allowed to pile up over the years. It is worth noting that Valve imposes a limit on the number of keys that someone can redeem in a short amount of time to somewhere around 48 keys per hour so if you are getting error messages for redeeming too many keys just allow it to cooldown for a little bit. If you have more detailed information regarding how many keys you can redeem in a short amount of time and if there is a way to circumvent this restriction I would love to hear from you.

Written by Luke Bender (lrbender01@gmail.com) in June 2021.