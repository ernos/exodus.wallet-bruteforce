#!/bin/python3
import argparse
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute-force Exodus wallet passwords using a wordlist.")
    parser.add_argument("wallet_path", help="Path to the Exodus wallet file (e.g., seed.seco)")
    parser.add_argument("wordlist_path", help="Path to the wordlist file containing passwords to try")
    parser.add_argument("--hash_path", help="Optional path to a hash file (not currently used)", default=None)

    args = parser.parse_args()

    bruteforce = ExodusBruteForcer(args.wallet_path, args.wordlist_path, args.hash_path)
    bruteforce.run()