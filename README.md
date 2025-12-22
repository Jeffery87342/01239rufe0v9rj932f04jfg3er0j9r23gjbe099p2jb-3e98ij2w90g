# Roblox Group Auto-Joiner 🚀

Fast and efficient Roblox group joining using the official Roblox API with multi-threading and proxy support.

## Features ✨

- ✅ **Fast Group Joining** - Uses Roblox's official API for quick joining
- ✅ **Multi-threaded** - Process multiple accounts simultaneously
- ✅ **Proxy Support** - Use proxies to avoid rate limits and IP bans
- ✅ **Cookie-based Authentication** - No need for usernames/passwords
- ✅ **Auto CSRF Token Handling** - Automatically manages Roblox security tokens
- ✅ **Color-coded Output** - Easy-to-read terminal output with status indicators
- ✅ **Detailed Statistics** - Shows success/failure counts and timing
- ✅ **Error Handling** - Robust error handling with informative messages

## Requirements 📋

- Python 3.7 or higher
- `requests` library

## Installation 🔧

1. **Clone or download this repository**

2. **Install Python** (if not already installed):
   - Windows: Download from [python.org](https://www.python.org/)
   - Linux: `sudo apt-get install python3 python3-pip`
   - macOS: `brew install python3`

3. **Install required package**:
   ```bash
   pip install requests
   ```

   Or just run `run.bat` (Windows) or `run.sh` (Linux/Mac) - it will auto-install dependencies.

## Usage 🎮

### Method 1: Using Launch Scripts (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

### Method 2: Direct Python Execution

```bash
python main.py
```
or
```bash
python3 main.py
```

### Configuration 📝

1. **Add your Roblox cookies to `cookies.txt`:**
   - One cookie per line
   - Get your cookie from browser (see below)
   
2. **(Optional) Add proxies to `proxies.txt`:**
   - One proxy per line
   - Supports multiple formats (see examples in file)

3. **Run the program and enter:**
   - Group ID you want to join
   - Number of threads (default: 5)

### How to Get Roblox Cookie 🍪

1. Log into Roblox on your browser
2. Press `F12` to open Developer Tools
3. Go to **Application** (Chrome) or **Storage** (Firefox)
4. Navigate to **Cookies** > `https://www.roblox.com`
5. Find `.ROBLOSECURITY` 
6. Copy the entire cookie value
7. Paste it into `cookies.txt`

**⚠️ WARNING:** Never share your cookie! It gives full access to your account.

## Proxy Formats 🌐

The tool supports multiple proxy formats in `proxies.txt`:

```
# HTTP Proxy
http://ip:port
http://user:pass@ip:port

# SOCKS5 Proxy
socks5://ip:port
socks5://user:pass@ip:port

# Auto-convert format
ip:port@user:pass
```

## Example Output 📊

```
╔══════════════════════════════════════════════════════════════════╗
║           Roblox Group Auto-Joiner v1.0                         ║
║           Fast group joining using Roblox API                   ║
╚══════════════════════════════════════════════════════════════════╝

Enter Roblox Group ID: 12345678
Enter number of threads (default 5): 10

[INFO] Loading cookies...
[SUCCESS] Loaded 50 cookies
[INFO] Loading proxies...
[SUCCESS] Loaded 20 proxies

======================================================================
Roblox Group Auto-Joiner
======================================================================
Group ID: 12345678
Total Accounts: 50
Threads: 10
Proxies Loaded: 20
======================================================================

[INFO] Processing: Username1 (ID: 123456789)
[Username1] Getting CSRF token...
[Username1] Joining group 12345678...
[Username1] ✓ Successfully joined group 12345678!

======================================================================
SUMMARY
======================================================================
✓ Success: 48
✗ Failed: 2
Total Processed: 50
Time Elapsed: 15.34 seconds
======================================================================
```

## Technical Details 🔧

### API Endpoints Used

- **Group Join:** `POST https://groups.roblox.com/v1/groups/{groupId}/users`
- **User Info:** `GET https://users.roblox.com/v1/users/authenticated`

### How It Works

1. Loads account cookies from `cookies.txt`
2. Optionally loads proxies from `proxies.txt`
3. For each account:
   - Retrieves user information
   - Gets CSRF token (Roblox security requirement)
   - Sends join request to group API
   - Reports success/failure
4. Processes accounts concurrently using thread pool
5. Displays summary statistics

### Security Features

- Uses HTTPS for all API calls
- Properly handles CSRF tokens
- Supports authenticated proxies
- No password storage required

## Troubleshooting 🔍

### "No cookies loaded"
- Make sure `cookies.txt` exists and contains valid cookies
- Check that cookies aren't expired
- Ensure one cookie per line

### "Failed with status code: 401"
- Cookie is invalid or expired
- Re-login to Roblox and get a fresh cookie

### "Failed with status code: 403"
- Account may be banned or restricted
- Group may have join restrictions
- Try using a proxy

### Proxy not working
- Check proxy format is correct
- Verify proxy is online and working
- For SOCKS proxies, install: `pip install pysocks requests[socks]`

## Rate Limits ⚠️

Roblox has rate limits to prevent abuse:
- Use proxies to distribute requests
- Adjust thread count if getting rate limited
- Add delays between batches if needed

## Legal Disclaimer ⚖️

This tool is for educational purposes only. Use at your own risk. The author is not responsible for:
- Account bans or restrictions
- Violation of Roblox Terms of Service
- Any misuse of this software

Always follow Roblox's Terms of Service and Community Guidelines.

## License 📄

MIT License - Feel free to modify and distribute

## Support 💬

If you encounter issues:
1. Check the troubleshooting section
2. Verify your cookies are valid
3. Test with a small number of accounts first
4. Check Roblox API status

---

**Note:** This tool uses Roblox's official API endpoints. Excessive use may result in rate limiting or account restrictions.
