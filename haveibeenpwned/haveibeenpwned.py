from bs4 import BeautifulSoup
import hashlib
import requests 
import sys 

BUFFER = 5


class Pwned(object):
    def __init__(self):
        self.api = "https://api.pwnedpasswords.com/range/"

    def password_occurences(self, password):
        """Check if a password has been pwned safely"""
        hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        return self.find_occurences(hash)

    def potential_matches(self, hash):
        """Retrieve list of potential matches from api using prefix of hash"""
        return BeautifulSoup(requests.get(self.api+hash[:BUFFER]).content, 'html.parser').text.split()

    def find_occurences(self, hash):
        """Search retrieved hash list for match"""
        hash_list = self.potential_matches(hash)
        for line in hash_list:
            hash_, occurences = line.split(":")
            if hash_ == hash[BUFFER:]:
                return int(occurences)
        return 0




if __name__ == "__main__":
    args = sys.argv 

    if len(args) != 2:
        print(f"Usage: {args[0]} <password>")
        exit()

    occurences = Pwned().password_occurences(args[1])

    if occurences > 0:
        print(f"Password has been PWNED: {occurences} occurences.")
    else:
        print("Password has not been pwned.")