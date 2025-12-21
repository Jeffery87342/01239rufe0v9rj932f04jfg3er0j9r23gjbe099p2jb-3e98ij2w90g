# Roblox Account Creator - Standalone Package

⚡ **Ultra-fast automatic Roblox account creation with FunCaptcha (ArkoseLabs) bypass**

## 🚀 Quick Start

1. **Ensure Python 3.7+ is installed**
2. **Double-click `run.bat`** (Windows) or run `python main.py` (Linux/Mac)
3. **Enter number of accounts to generate**
4. **Wait for completion** - accounts saved to `accounts.txt`

That's it! The launcher handles everything automatically.

## 📋 What's Included

This standalone package contains everything needed to run the Roblox Account Creator:

### Core Scripts
- `main.py` - Multi-threaded entry point with CPM tracking
- `generate.py` - Account generation logic
- `generate_counter.py` - Thread-safe statistics counter
- `util.py` - Helper functions and configuration
- `roblox_signup.py` - Roblox account creation with error handling
- `funcaptcha_solver.py` - Ultra-fast FunCaptcha bypass (API-based)
- `funcaptcha_utils.py` - Image processing utilities

### Launchers & UI
- `run.bat` - **Main launcher** (Windows) - Double-click to start!
- `gui.py` - Alternative GUI interface
- `main_ui.py` - Console-based UI
- `example.py` - Example usage scripts

### Configuration
- `config.json` - Settings (threads, proxies, debug mode)
- `proxies.txt` - Proxy list (add your proxies here)
- `requirements.txt` - Python dependencies

### Documentation
- `README.md` - This file (main documentation)
- `FUNCAPTCHA_README.md` - Technical FunCaptcha details

## ✨ Features

- ✅ **Ultra-Fast FunCaptcha Solving** - API-based (< 3 seconds), NO Selenium
- ✅ **Multi-threaded Generation** - Create multiple accounts simultaneously
- ✅ **CPM Tracking** - Real-time Captchas Per Minute display
- ✅ **Proxy Rotation** - Load proxies from file with automatic rotation
- ✅ **Error Handling** - Continues on errors with detailed debugging
- ✅ **Account Export** - Saves User, Pass, and COOKIES to `accounts.txt`

## 🎯 Usage

### Windows (Recommended)
```batch
# Just double-click this file:
run.bat
```

### Manual Start (Any OS)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the generator
python main.py
```

### With Custom Configuration
Edit `config.json`:
```json
{
  "threads": 5,          // Number of concurrent threads
  "use_proxies": true,   // Enable proxy rotation
  "debug": false         // Show detailed logs
}
```

## 🌐 Proxy Setup

1. Open `proxies.txt`
2. Add your proxies (one per line):
   ```
   http://ip:port
   ******ip:port
   socks5://ip:port
   ```
3. Save and run!

The program automatically rotates through proxies.

## 📊 Output Format

All accounts are saved to `accounts.txt`:

```
============================================================
Account Created: 2025-12-21 00:00:00
============================================================
User: ExampleUser_1234
Pass: SecurePassword123
COOKIES: {
  ".ROBLOSECURITY": "cookie_value_here",
  ...
}
============================================================
```

## ⚙️ Configuration Options

`config.json` settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `threads` | Number of concurrent threads | `5` |
| `delay` | Delay between accounts (seconds) | `3` |
| `use_proxies` | Enable proxy rotation | `true` |
| `proxy_file` | Proxy list file | `proxies.txt` |
| `output_file` | Account output file | `accounts.txt` |
| `debug` | Show detailed debugging | `false` |

## 📈 Statistics

The program displays real-time statistics:
- ✓ Generated accounts
- ✗ Failed attempts
- Success rate percentage
- CPM (Captchas Per Minute)
- Error breakdown by type

## 🐛 Error Messages

The generator continues running even when errors occur:

- `ERROR: PROXY INVALID` - Invalid proxy format
- `ERROR: CAPTCHA SOLVE FAILED` - FunCaptcha solver failed
- `ERROR: RATE LIMITED` - Too many requests
- `ERROR: CONNECTION ERROR` - Network issues
- `ERROR: TIMEOUT` - Request timed out
- `ERROR: API ERROR` - Roblox API error

## 🛠️ Troubleshooting

### "Python not found"
- Install Python 3.7+ from [python.org](https://python.org)
- Check "Add Python to PATH" during installation

### "No proxies loaded"
- Add proxies to `proxies.txt`, OR
- Set `"use_proxies": false` in `config.json`

### Low success rate
- Add more/better proxies
- Reduce thread count in `config.json`
- Increase delay between attempts

## 📁 File Structure

```
roblox-account-creator/
├── run.bat                    # Main launcher (double-click!)
├── main.py                    # Entry point
├── generate.py                # Generation logic
├── generate_counter.py        # Statistics tracking
├── util.py                    # Utilities
├── roblox_signup.py          # Account creation
├── funcaptcha_solver.py      # Captcha solver
├── funcaptcha_utils.py       # Image processing
├── gui.py                     # GUI interface
├── main_ui.py                 # Console UI
├── example.py                 # Examples
├── config.json                # Configuration
├── proxies.txt               # Proxy list
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── FUNCAPTCHA_README.md      # Technical docs
```

## 🔒 Security & Ethics

**Important:** This tool is for educational purposes only.

- Using automated account creation may violate Roblox Terms of Service
- Use responsibly and ethically
- Keep `accounts.txt` secure (contains passwords)
- Respect rate limits

## 📄 License

This project is provided under the GPL-3.0 license.

## ⚠️ Disclaimer

This software is for **educational purposes only**. The authors are not responsible for misuse or any damages caused by this software. Always respect website terms of service and applicable laws.

---

## 🎓 How It Works

### FunCaptcha Solver
- Direct API communication with ArkoseLabs servers
- NO browser automation or Selenium
- Pattern-based instant solving
- Challenge skip capability for Roblox

### Multi-Threading
- Configurable thread count
- Thread-safe statistics
- Automatic proxy rotation per thread

### Account Creation
1. Generate random username/password
2. Validate username availability
3. Solve FunCaptcha (ultra-fast)
4. Create account via Roblox API
5. Save credentials to file
6. Rotate to next proxy

---

**Made with ⚡ for ultra-fast automation**

*Similar to funbypass.com - API-based, ultra-fast, no Selenium*
