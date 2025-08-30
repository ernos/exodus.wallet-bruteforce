"""
You are an expert scripter and programmer in python with an extensive knowledge of cryptography.
"""
# 1.Project Objective and goals #
We are building a Python program to brute force the password for an Exodus offline wallet. The user has lost 
their password but knows their own password style. We can likely determine the cryptography used by Exodus wallets. 
A reference Python script is available that takes a password hash and wallet file, and returns the 12-word seed for 
key regeneration. Use this file for cryptographic study, as Exodus is not open source. See `exodus-decode-wallet.py`
for reference.


## 1.1 File structure ##
 `.github/`
    `.github/copilot-instructions.md` - This file. Your guidelines for all interactions.
    `.github/exodus-decode-wallet.py` - Reference file to study how exodus uses cryptography in their wallets
    `.vscode/`
    `.vscode/.launch`
    `.vscode/.tasks`
 `.gitignore`
 `start.py`                 -  Main file which will generate a wordlist from users criterea of style of passwords,
                                    load the encrypted wallet file and try to either decrypt it or generate the seed
                                    whicever takes less time and computing power.
 `wordlist.py`             -  A class that handles wordlist generation. It should help guide the user how to make
                                an effective wordlist generator, possibly by simply asking the user to input 10+ of 
                                his own passwords which are similar looking and then creating an algorithm to generate
                                a wordlist from the patterns learned from that.
 ``

## 2.Project libraries and dependencies ##
"""
Help fill out the dependencies list after analyzing the project and deciding on the best approach.
"""

# 2.Template instructions to follow for all answers involving code generation or project planning #
 """ 
 You should reference these instructions in all answers you create that are not just simple yes/no or
 short question-queries. Every queries involving code generation more than 10-20 lines or big changes to
 the project such as implementing new libraries or new concepts for your client """
 ## 2.2 Guidelines to follow ##
 - Think about the full picture and scope before answering.
 - Read the user's objective/question twice: first for understanding, second for planning and structuring your response.
 - Ensure you have reviewed all relevant reference code and library documentation before starting.
 - Optimize new code for clarity and efficiency.
 - Review new code snippets/functions at least once after writing.
 - Use clear variable names and structure.
 - Close file objects when not needed.
 - Isolate new functionality for testing.
 - If implementing new features, provide tips for isolating functions to speed up debugging/testing.
 - Analyze the user's goal.
 - Don't blindly follow instructions; consider the end goal and suggest more effective solutions if possible.
    
