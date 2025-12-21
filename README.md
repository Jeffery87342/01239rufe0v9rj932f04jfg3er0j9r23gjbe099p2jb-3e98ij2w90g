# Roblox Account Creator - FunCaptcha Bypass

⚡ **Ultra-fast automatic Roblox account creation with FunCaptcha (ArkoseLabs) bypass**

---

## 🚀 Quick Start

**Just double-click `run.bat`!** (Windows)

Or manually:
```bash
pip install -r requirements.txt
python main.py
```

That's it! The launcher handles everything automatically.

---

## ✨ Key Features

- ✅ **Ultra-Fast FunCaptcha Solving** - API-based (like funbypass.com), NO Selenium
- ✅ **Multi-threaded Generation** - Create multiple accounts simultaneously  
- ✅ **CPM Tracking** - Real-time Captchas Per Minute display in console title
- ✅ **Proxy Rotation** - Load proxies from `proxies.txt` with automatic rotation
- ✅ **Error Handling** - Continues on errors with detailed debugging
- ✅ **Account Export** - Saves User, Pass, and COOKIES to `accounts.txt`
- ✅ **Single-Click Launch** - Just run `run.bat`!

---

## 📋 What's Included

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
- `README.md` - This file
- `FUNCAPTCHA_README.md` - Technical FunCaptcha details

---

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

### Configuration

Edit `config.json`:
```json
{
  "threads": 5,          // Number of concurrent threads
  "delay": 3,            // Delay between accounts (seconds)
  "use_proxies": true,   // Enable/disable proxy rotation
  "debug": false         // Show detailed debugging
}
```

### Proxy Setup

Add proxies to `proxies.txt` (one per line):
```
http://ip:port
******proxy.com:port
socks5://ip:port
```

The program automatically rotates through proxies!

---

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

---

## 📈 Features Breakdown

### Multi-Threading
- Configurable thread count (default: 5 threads)
- Thread-safe statistics tracking
- Concurrent account generation
- CPM (Captchas Per Minute) displayed in console title

### Error Handling & Debugging
The generator **continues running even when errors occur**, displaying specific error messages:
- `ERROR: PROXY INVALID` - Invalid proxy format
- `ERROR: CAPTCHA SOLVE FAILED` - FunCaptcha solver failed
- `ERROR: RATE LIMITED` - Too many requests
- `ERROR: CONNECTION ERROR` - Network issues
- `ERROR: TIMEOUT` - Request timed out
- `ERROR: API ERROR` - Roblox API error

All errors are tracked and displayed in final statistics with error breakdown!

### FunCaptcha Solver
- **Ultra-fast API-based solving** (< 3 seconds)
- **NO Selenium** - Pure API communication
- Functions like funbypass.com
- Challenge skip capability for Roblox
- Pattern-based instant solving

---

## 📁 File Structure

```
roblox-account-creator/
├── run.bat                    # Main launcher (double-click!)
├── main.py                    # Multi-threaded entry point
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

---

## 🛠️ Requirements

- **Python 3.7+**
- Internet connection
- Windows (for .bat launcher) or any OS (manual start)

### Dependencies

All dependencies in `requirements.txt`:

- `requests` - HTTP library
- `pillow` - Image processing
- `numpy` - Numerical operations
- `opencv-python` - Computer vision
- `colorama` - Colored console output

**Installation:** `pip install -r requirements.txt`

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python 3.7+ from [python.org](https://python.org)
- Check "Add Python to PATH" during installation

### Installation errors (numpy/opencv build failures on Windows)
If you get errors about missing compilers when running `pip install -r requirements.txt`:

**Quick Fix:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install packages one at a time (this uses pre-built wheels)
pip install requests
pip install pillow
pip install "numpy<2.0.0"
pip install opencv-python
pip install colorama
```

**Alternative:** The `run.bat` launcher handles this automatically. Just double-click `run.bat` instead of manually installing.

### "No proxies loaded"
- Add proxies to `proxies.txt`, OR
- Set `"use_proxies": false` in `config.json`

### Low success rate
- Add more/better proxies
- Reduce thread count in `config.json`
- Increase delay between attempts

### Errors continue
- This is normal! The generator continues despite errors
- Check error breakdown in statistics for patterns
- Adjust config based on error types

---

## 📊 Statistics Display

The program shows real-time statistics:
```
═══════════════════════════════════════════════════════════
                     LIVE STATISTICS
═══════════════════════════════════════════════════════════
✓ Generated:      25
✗ Failed:         3
Total Attempts:   28
Success Rate:     89.3%
CPM:              12
Elapsed:          00:02:05

Error Breakdown:
  • RATE LIMITED: 2
  • TIMEOUT: 1
═══════════════════════════════════════════════════════════
```

Console title updates every second: `Elapsed: 00:02:05 | Generated: 25 | Failed: 3 | CPM: 12`

---

## ⚙️ Advanced Configuration

### Adjust Thread Count
Higher threads = faster generation (but more resource usage):
```json
{
  "threads": 10  // Increase for faster generation
}
```

### Enable Debug Mode
See detailed logs for each step:
```json
{
  "debug": true
}
```

### Disable Proxies
Run without proxies (not recommended for bulk):
```json
{
  "use_proxies": false
}
```

---

## 🎓 How It Works

### Architecture

1. **Multi-threading** - Spawns configurable worker threads
2. **Proxy Rotation** - Each thread gets a different proxy
3. **Username Generation** - Random unique usernames
4. **FunCaptcha Solving** - Ultra-fast API-based bypass
5. **Account Creation** - Direct Roblox API calls
6. **Data Export** - Saves to accounts.txt with User/Pass/COOKIES
7. **Statistics Tracking** - Thread-safe counter for CPM/stats

### FunCaptcha Solver Implementation

Direct API communication with ArkoseLabs endpoints - no browser automation:

```python
solver = FunCaptchaSolver(
    public_key="476068BF-9607-4799-B53D-966BE98E2B81",
    service_url="https://client-api.arkoselabs.com",
    page_url="https://www.roblox.com",
    proxy=proxy,
    debug=False
)
token = solver.solve()  # Returns session token in <3s
```

Pattern-based solving with challenge skip capability for Roblox-specific implementations.

---

## 🔒 Security & Ethics

**Important:** This tool is for educational purposes only.

- Using automated account creation may violate Roblox Terms of Service
- Use responsibly and ethically
- Keep `accounts.txt` secure (contains passwords and cookies)
- Respect rate limits
- Use proxies to avoid detection

---

## 📄 License

This project is licensed under GPL-3.0-or-later. See LICENSE file for details.

## ⚠️ Disclaimer

This software is for **educational purposes only**. The authors are not responsible for misuse or any damages caused by this software. Always respect website terms of service and applicable laws.

---

**Made with ⚡ for ultra-fast automation**

*Similar to funbypass.com - API-based, ultra-fast, no Selenium*
