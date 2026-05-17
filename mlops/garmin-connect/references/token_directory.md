# Custom Token Directory Configuration

The `garminconnect` library stores OAuth tokens in a directory determined by the `HOME` environment variable (specifically, `$HOME/.garminconnect`). In some environments (e.g., WSL with a custom Hermes home, containerized setups, or when `$HOME` is overridden), the token files may end up in an unexpected location.

## How to Determine the Current Token Directory

You can check where the library is looking for tokens by running:

```bash
python3 -c "import os; print(os.path.expanduser('~/.garminconnect'))"
```

## Options to Specify a Custom Token Directory

### Option 1: Set the HOME Environment Variable (Not Recommended)
Changing `HOME` can affect many other applications. Only do this if you understand the implications.

```bash
export HOME=/custom/path   # Then .garminconnect will be under $HOME/.garminconnect
```

### Option 2: Explicitly Set TOKEN_DIR in Your Scripts
In any script that uses `garminconnect`, define `TOKEN_DIR` explicitly and pass it to the token loading/saving functions.

Example:

```python
import os
TOKEN_DIR = '/path/to/your/token/directory'   # e.g., '/home/mataanek/.hermes/.garminconnect'
# ... then use TOKEN_DIR when loading and saving tokens
```

### Option 3: Use a Symbolic Link
If you cannot change the script, you can make the expected directory a symlink to where the tokens actually are:

```bash
ln -s /actual/token/location ~/.garminconnect
```

## Recommendation for Hermes Agent Users

Given that Hermes Agent may set a custom `HOME` (as seen in the session where `HOME` was `/home/mataanek/.hermes/home`), it is most reliable to:

1. After the initial interactive login, note the actual directory where the tokens were saved (the script will print it).
2. In your persistent connection script, set `TOKEN_DIR` to that directory.
3. Alternatively, copy the tokens to the directory that the script expects (as indicated by the printed path from the one-liner).

The interactive login one-liner in `references/interactive_login_one_liner.md` already prints the token directory after saving. Use that output to configure your scripts accordingly.