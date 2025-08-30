# Project Steps for Exodus Wallet Password Brute Forcer

## 1. Analyze the Problem and Reference Code
- Review `exodus-decode-wallet.py` to understand Exodus wallet encryption and seed/private key derivation.
- Identify cryptographic algorithms used (e.g., AES, PBKDF2, Scrypt).
- Determine required inputs for decryption (password, wallet file).

## 2. Wordlist Generation
- Implement or improve `createwordlist.py` to generate a wordlist based on your password style.
- Use user input (10+ similar passwords) to learn patterns and generate candidate passwords.
- Consider Markov chains, regex, or heuristics for password pattern extraction.

## 3. Brute Force/Decryption Logic
- In `start.py`, load the wallet file and iterate through the generated wordlist.
- For each password, attempt decryption using the reference method.
- If successful, extract the 12-word seed or private key.

## 4. Dependencies and Libraries
- List required libraries (e.g., `pycryptodome`, `bip39`) after analyzing the reference code.
- Keep project modular: wordlist generation, wallet decryption, and result handling as separate components.

## 5. Testing and Optimization
- Isolate decryption logic for easy testing.
- Optimize wordlist generation for speed and relevance.

## Next Steps
1. Review reference code for cryptographic details.
2. Design wordlist generator logic in `createwordlist.py`.
3. Implement brute force loop in `start.py`.
4. Document and list dependencies.
