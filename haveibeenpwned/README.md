# HaveIBeenPwned Python3 Script
This Python script is used to check if your password has been leaked using the api from https://haveibeenpwned.com ****without having to worry about sending your raw password to the website.****
Instead the script uses a segment of the hash of your password to check against the haveibeenpwned database.
The result is the amount of times your password has appeared in various leaks.

Check out the HaveIBeenPwned API here: https://haveibeenpwned.com/API/v3
The technique used by the script is specified here: https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange

## Usage
Clone or download ****haveibeenpwned.py**** then run
```
python3 haveibeenpwned.py <password>
```
