#!/bin/python3
from exoduswalletreader import ExodusWalletReader
from wordlist import WordlistGenerator


class ExodusBruteForcer:
    def __init__(self, wallet_path, wordlist_path, hash_path=None):
        self.wallet_path = wallet_path
        self.wordlist_path = wordlist_path
        self.hash_path = hash_path

    def try_password(self, password):
        try:
            reader = ExodusWalletReader(self.wallet_path)
            result = reader.decrypt(password)
            if result['status']:
                mnemonic = ExodusWalletReader.extractMnemonic(result)
                print(f"Success! Password: {password}, Seed: {mnemonic}")
                return True
        except Exception:
            pass
        return False

    def run(self):
        with open(self.wordlist_path) as f:
            for password in f:
                password = password.strip()
                print(f"Trying password: {password}")
                if self.try_password(password):
                    print(f"FOUND THE PASSWORD! Password is:\"{password}\"")
                    break  # Stop on first success, or continue for all
                
bruteforce = ExodusBruteForcer("wallet/storage.seco", "wordlist.txt")

bruteforce.run()