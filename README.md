# Doge Unblocker V4 (MODIFIED) + Roblox Account Creator

This repository contains **Doge Unblocker V4** web proxy plus a powerful **Roblox Account Creator** with ultra-fast FunCaptcha bypass.

---

## 🎮 Doge Unblocker - Web Proxy

Doge Unblocker is a lightning-fast web proxy designed for performance and stealth. We are **by far** the best proxy, offering speeds and features unbeatable by any other proxies.

### Proxy Features:
- Advanced Tab Cloaking
- Advanced About:Blank Cloaking
- Hiding site from browser history
- Clickoff Cloaking
- Automatic URL Cloaking
- Customizable/Personalization features
- Access settings easily (right-click)
- Authentication
- Extremely clean UI
- A powerful web proxy
- A large selection of Apps & Games
- Many more

---

## 🤖 Roblox Account Creator - FunCaptcha Bypass

**⚡ Ultra-fast automatic Roblox account creation with FunCaptcha (ArkoseLabs) bypass**

### Key Features:
- ✅ **Ultra-Fast FunCaptcha Solving** - API-based (like funbypass.com), NO Selenium
- ✅ **Multi-threaded Generation** - Create multiple accounts simultaneously  
- ✅ **CPM Tracking** - Real-time Captchas Per Minute display
- ✅ **Proxy Rotation** - Load proxies from file with automatic rotation
- ✅ **Error Handling** - Continues on errors with detailed debugging
- ✅ **Account Export** - Saves User, Pass, and COOKIES to `accounts.txt`
- ✅ **Single-Click Launch** - Just run `run.bat`!

## 🚀 Quick Start - Account Creator

### Installation

**Just double-click `run.bat`!**

The launcher automatically:
1. ✓ Checks for Python
2. ✓ Creates virtual environment
3. ✓ Installs dependencies
4. ✓ Starts the application

### Usage

1. **Run the launcher**: Double-click `run.bat`
2. **Enter account count**: How many accounts to generate?
3. **Wait for completion**: Accounts are created automatically
4. **Check output**: All accounts saved to `accounts.txt`

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
http://user:pass@proxy.com:port
```

The program automatically rotates through proxies!

### Output Format

`accounts.txt` contains:
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

## 📊 Features Breakdown

### Multi-Threading
- Configurable thread count (default: 5 threads)
- Thread-safe statistics tracking
- Concurrent account generation

### CPM (Captchas Per Minute) Tracking
- Real-time CPM display in console title
- Elapsed time tracking
- Average time per account

### Error Handling & Debugging
The generator **continues running even when errors occur**, displaying:
- `ERROR: PROXY INVALID` - Invalid proxy format
- `ERROR: CAPTCHA SOLVE FAILED` - FunCaptcha solver failed
- `ERROR: RATE LIMITED` - Too many requests
- `ERROR: CONNECTION ERROR` - Network issues
- `ERROR: TIMEOUT` - Request timed out
- `ERROR: API ERROR` - Roblox API error

Errors are tracked and displayed in final statistics!

### FunCaptcha Solver
- **Ultra-fast API-based solving** (< 3 seconds)
- **NO Selenium** - Pure API communication
- Functions like funbypass.com
- Challenge skip capability for Roblox
- Pattern-based instant solving

## 📁 Project Structure

### Account Creator Files:
- `run.bat` - **Main launcher** (double-click to start)
- `main.py` - Multi-threaded entry point with CPM tracking
- `generate.py` - Account generation logic
- `generate_counter.py` - Thread-safe statistics counter
- `util.py` - Helper functions and config management
- `roblox_signup.py` - Roblox account creation with error handling
- `funcaptcha_solver.py` - Ultra-fast FunCaptcha bypass
- `funcaptcha_utils.py` - Image processing utilities
- `config.json` - Configuration file
- `proxies.txt` - Proxy list (optional)
- `accounts.txt` - Generated accounts (auto-created)
- `requirements.txt` - Python dependencies

### Web Proxy Files:
- `index.js` - Express server
- `static/` - Web proxy files
- `package.json` - Node dependencies

## 🛠️ Requirements

### Account Creator:
- **Python 3.7+**
- Internet connection
- Windows (for .bat launcher)

### Web Proxy:
- **Node.js 16+**
- npm 7+

## 💻 Installation Details

### Account Creator Dependencies:
```bash
pip install -r requirements.txt
```

Includes:
- `requests` - HTTP library
- `pillow` - Image processing
- `numpy` - Numerical operations
- `opencv-python` - Computer vision
- `colorama` - Colored console output

### Web Proxy Dependencies:
```bash
npm install
```

## 🎯 Usage Examples

### Generate 10 Accounts:
```bash
run.bat
# Enter: 10
```

### Generate with Custom Threads:
Edit `config.json`:
```json
{
  "threads": 10
}
```

### Use Proxies:
Add to `proxies.txt`:
```
http://proxy1.com:8080
http://proxy2.com:3128
```

## 📈 Statistics Display

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

## 🔒 Security & Ethics

**Important:** This tool is for educational purposes only.

- Using automated account creation may violate Roblox Terms of Service
- Use responsibly and ethically
- Keep `accounts.txt` secure (contains passwords)
- Respect rate limits
- Use proxies to avoid detection

## ⚙️ Advanced Configuration

### Adjust Thread Count:
Higher threads = faster generation (but more resource usage)
```json
{
  "threads": 10  // Increase for faster generation
}
```

### Enable Debug Mode:
See detailed logs for each step:
```json
{
  "debug": true
}
```

### Disable Proxies:
Run without proxies (not recommended for bulk):
```json
{
  "use_proxies": false
}
```

## 🐛 Troubleshooting

### "Python not found"
- Install Python 3.7+ from python.org
- Check "Add Python to PATH" during installation

### "No proxies loaded"
- Add proxies to `proxies.txt`
- Or set `"use_proxies": false` in config.json

### Low success rate
- Add more/better proxies
- Reduce thread count
- Increase delay between attempts

### Errors continue
- This is normal! The generator continues despite errors
- Check error breakdown for patterns
- Adjust config based on error types

## 📞 Support

For issues:
1. Check this README
2. Verify all requirements
3. Check `config.json` settings
4. Review error messages in statistics

---

## Current Developers:
- [Derpman](https://github.com/DerpmanDev)
- [KDust7](https://github.com/KDust7)

## Deployment (Web Proxy)
[![Deploy on Railway](https://binbashbanana.github.io/deploy-buttons/buttons/remade/railway.svg)](https://railway.app/template/h7StcI?referralCode=u82tqg)
<a href="https://render.com/deploy?repo=https://github.com/dogenetwork/doge-unblocker">
<img src="https://raw.githubusercontent.com/BinBashBanana/deploy-buttons/main/buttons/remade/render.svg"></img></a>
<a href="https://app.cyclic.sh/api/app/deploy/dogenetwork/v4">
<img src="https://camo.githubusercontent.com/607221ca4be547dd929fca7c997a93dfaf1f7b06a1baacaf25b44cf5405c9f91/68747470733a2f2f62696e6261736862616e616e612e6769746875622e696f2f6465706c6f792d627574746f6e732f627574746f6e732f72656d6164652f6379636c69632e737667"></img></a>
[![Deploy with Vercel](https://binbashbanana.github.io/deploy-buttons/buttons/remade/vercel.svg)](https://vercel.com/new/clone?repositoryurl=https://github.com/dogenetwork/v4)
[![Deploy to Koyeb](https://binbashbanana.github.io/deploy-buttons/buttons/remade/koyeb.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/dogenetwork/v4)

### Discord
[![Join us on Discord](https://invidget.switchblade.xyz/sWPHCdxCPU?theme=dark)](https://discord.gg/sWPHCdxCPU)

---

## ⚖️ License

This project is licensed under GPL-3.0-or-later.

## ⚠️ Disclaimer

**Account Creator:** This software is for educational purposes only. The authors are not responsible for misuse. Automated account creation may violate website Terms of Service. Use at your own risk.

**Web Proxy:** Use responsibly and in compliance with applicable laws and regulations.

---

**Made with ⚡ for ultra-fast automation**
