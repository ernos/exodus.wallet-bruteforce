# Exodus Wallet Brute-Force Cracker

A Python-based tool for brute-forcing passwords on Exodus wallet files. This program attempts to decrypt Exodus wallet seeds using a generated wordlist of potential passwords. It is capable of creating pretty advanced wordlist based on regex inputs. 

## Disclaimer

**WARNING:** This tool is intended for educational and ethical purposes only. Attempting to crack passwords without authorization may be illegal and unethical. Use this tool only on wallets you own or have explicit permission to access. The author is not responsible for any misuse.

## Features

- Brute-force password cracking for Exodus wallet files
- Wordlist generation from templates or password samples
- Support for complex password patterns with ranges, alternations, and quantifiers
- Modular design with separate components for reading wallets and generating wordlists

## Requirements

- Python 3.6+
- Required Python packages:
  - `mnemonic`
  - `pycryptodome`

1. Create a virtual environment. I like to have this in my .bashrc and use this, or you can just paste it in console and call it.
   """
   create_and_activate_venv_here() {
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        echo "Usage: create_and_activate_venv_here [venv_dir]"
        echo ""
        echo "Creates a Python virtual environment in the specified directory and activates it."
        echo "If venv_dir is not provided, it defaults to '.venv'."
        echo ""
        echo "Requirements:"
        echo "  - Python 3 must be installed and available in PATH."
        echo ""
        echo "Examples:"
        echo "  create_and_activate_venv_here          # Creates and activates .venv"
        echo "  create_and_activate_venv_here myenv    # Creates and activates myenv"
        return 0
    fi

    local venv_dir="${1:-.venv}"
    local python_bin="$(command -v python3)"

    if [[ -z "$python_bin" ]]; then
        echo "Python3 not found in PATH."
        return 1
    fi

    if [[ -d "$venv_dir" ]]; then
        echo "Virtual environment '$venv_dir' already exists."
    else
        "$python_bin" -m venv "$venv_dir"
        if [[ $? -ne 0 ]]; then
            echo "Failed to create virtual environment."
            return 2
        fi
        echo "Virtual environment created at ./$venv_dir"
    fi

    source "$venv_dir/bin/activate"
    if [[ $? -ne 0 ]]; then
        echo "Failed to activate virtual environment."
        return 3
    fi

    echo -e "Virtual environment: $1 has been created and activated.\nPath to venv: $venv_dir."
}
create_and_activate_venv_here
"""
Put in .bashrc, reload with "source ~/.bashrc"
Install dependencies with:

```bash
create_and_activate_venv_here
pip3 install -r requirements
./bruteforce.py
```

## Files

- `bruteforce.py`: Main brute-force script that tries passwords from a wordlist against the wallet file
- `exoduswalletreader.py`: Library for reading and decrypting Exodus wallet files
- `wordlist.py`: Wordlist generator that creates password lists from templates or samples
- `wordlist.txt`: Generated wordlist file (created by wordlist.py)
- `wordinput.txt`: Input file containing password templates
- `wallet/`: Directory containing wallet files
  - `seed.seco`: Encrypted seed file
  - `storage.seco`: Storage file
  - `passwordinfo.txt`: Password information (if available)

## Usage

### 1. Prepare Your Wordlist

Generate a wordlist using templates or samples:

```bash
# Generate from a template
python wordlist.py --template "password[0-9]{1,3}"

# Generate from samples in a file
python wordlist.py --input samples.txt --input-type samples

# Use configuration file
python wordlist.py --config wordlist_config.json
```

Templates support:

- Ranges: `[0-9]`, `[a-z]`
- Alternations: `[a|b|c]`
- Repetition: `[0-9]{1,3}`
- Quantifiers: `[&]?`, `[&]*`, `[&]+`

### 2. Run the Brute-Force

```bash
python bruteforce.py
```

The script will:

- Load passwords from `wordlist.txt`
- Attempt to decrypt `wallet/seed.seco` with each password
- Print progress and stop when a valid password is found
- Display the recovered mnemonic seed phrase

## Configuration

Create a `wordlist_config.json` file for advanced configuration:

```json
{
  "samples": ["password1", "letmein"],
  "template": "word[0-9]{1,2}",
  "max_count": 10000
}
```

## Known Issues

- Bug in `wordlist.py` lines 247-251: Quantifiers like `[&]?` are not correctly parsed when embedded within words. For example, `"pass[&]?word"` should generate `"pass&word"` and `"password"`, but currently produces incorrect results.

## Contributing

This is a personal project. Pull requests and issues are welcome for bug fixes and improvements.

## License

This project is provided as-is without warranty. See individual file headers for licensing information.