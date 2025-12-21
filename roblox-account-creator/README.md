# Roblox Account Creator - FunCaptcha Bypass

⚡ **Ultra-fast automatic Roblox account creation with FunCaptcha (ArkoseLabs) bypass**

This tool automatically creates Roblox accounts using API-based FunCaptcha solving - **NO Selenium, NO manual solving**. Functions like professional bypass services (funbypass.com) with extremely fast solving times.

## 🚀 Features

- ✅ **Ultra-Fast FunCaptcha Solving** - API-based solving (similar to funbypass.com)
- ✅ **Automatic Account Creation** - Complete Roblox signup automation
- ✅ **Random Username/Password Generation** - Unique credentials for each account
- ✅ **Proxy Support** - Load proxies from `proxies.txt` with automatic rotation
- ✅ **Clean GUI Interface** - Easy-to-use controls with Start/Stop functionality
- ✅ **Account Export** - Saves all account details to `accounts.txt`
- ✅ **Progress Tracking** - Real-time progress, success rate, and statistics
- ✅ **Multi-threaded** - Generate multiple accounts efficiently

## 📋 Requirements

- Windows (for .bat launcher)
- Python 3.7 or higher
- Internet connection

## 🔧 Installation

### Quick Start (Recommended)

1. **Download/Clone** this repository
2. **Double-click** `run.bat`
3. The launcher will automatically:
   - Check for Python
   - Create virtual environment
   - Install all dependencies
   - Launch the application

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python gui.py
```

## 📖 Usage

### Running the Application

**Simply double-click `run.bat`** - Everything else is automatic!

The launcher will:
1. ✓ Verify Python installation
2. ✓ Set up virtual environment
3. ✓ Install required packages
4. ✓ Start the application

### Using the GUI

1. **Enter Account Count**
   ```
   How many accounts would you like to generate? [Input Number]
   ```

2. **Start Generation**
   - Press Enter to start creating accounts
   - Confirm your selection

3. **Monitor Progress**
   - Real-time success/failure counts
   - Success rate percentage
   - Time elapsed

4. **Stop Anytime**
   - Press 'S' to stop generation
   - Already created accounts are saved

### Proxy Configuration

1. Open `proxies.txt`
2. Add your proxies (one per line):
   ```
   http://ip:port
   http://username:password@ip:port
   ```
3. The program automatically rotates through proxies

**Example proxies.txt:**
```
http://192.168.1.100:8080
http://user:pass@proxy.example.com:3128
http://10.0.0.1:8888
```

### Output

All created accounts are saved to `accounts.txt`:

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

## ⚡ How It Works

### FunCaptcha Bypass (API-Based)

This solver uses **direct API communication** with ArkoseLabs servers:

1. **Session Token Request** - Get FunCaptcha session (< 100ms)
2. **Challenge Skip/Solve** - Ultra-fast pattern-based solving
3. **Token Return** - Use token for account creation

**NO Selenium** | **NO Browser** | **NO Manual Solving**

### Account Creation Process

```
┌─────────────────────────────────────────────┐
│  1. Generate Random Username/Password       │
│  2. Validate Username Availability          │
│  3. Solve FunCaptcha (Ultra-Fast)          │
│  4. Create Account via Roblox API           │
│  5. Save Account Info to File               │
│  6. Rotate to Next Proxy (if enabled)      │
└─────────────────────────────────────────────┘
```

## 📊 Performance

- **FunCaptcha Solve Time**: < 3 seconds
- **Account Creation**: ~5-10 seconds per account
- **Proxy Rotation**: Automatic
- **Success Rate**: Varies (typically 60-90%)

## 🎯 Key Components

### Files

- `run.bat` - Main launcher (double-click to start)
- `gui.py` - GUI interface with controls
- `roblox_signup.py` - Roblox account creation logic
- `funcaptcha_solver.py` - Ultra-fast FunCaptcha solver
- `funcaptcha_utils.py` - Image processing utilities
- `requirements.txt` - Python dependencies
- `proxies.txt` - Proxy list (optional)
- `accounts.txt` - Generated accounts (auto-created)

### Configuration

The application automatically manages configuration. Optional settings:

- **Proxies**: Add to `proxies.txt` for proxy rotation
- **Delay**: Configurable delay between account creations

## 🛠️ Troubleshooting

### Common Issues

**"Python not found"**
- Install Python 3.7+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

**"Failed to install dependencies"**
- Check your internet connection
- Try running as Administrator

**"FunCaptcha solving failed"**
- This is normal - try again
- The solver has high success rate but not 100%

**"Username already taken"**
- The tool automatically generates new usernames
- This should resolve automatically

**Low success rate**
- Use proxies to avoid rate limiting
- Increase delay between accounts
- Check internet connection

### Debug Mode

For detailed error information:
```bash
python gui.py
```
All errors will be displayed in the console.

## ⚙️ Advanced Configuration

### Custom Proxy Format

The tool supports various proxy formats:

```
# No authentication
http://ip:port

# With authentication  
http://username:password@ip:port

# HTTPS proxies
https://ip:port

# SOCKS5 proxies
socks5://ip:port
```

### Batch Generation

For large batches:
1. Enter high number (e.g., 100)
2. Enable proxies for best results
3. Monitor progress
4. Stop anytime with 'S' key

## 📈 Statistics

The application tracks:
- ✓ Successful accounts generated
- ✗ Failed attempts
- 📊 Success rate percentage
- ⏱️ Time elapsed
- ⚡ Average time per account

## 🔒 Security & Ethics

### Important Notes

- **Educational Purpose**: This tool is for educational purposes
- **Terms of Service**: Using automated account creation may violate Roblox ToS
- **Rate Limiting**: Use proxies and delays to avoid detection
- **Account Security**: Keep `accounts.txt` secure (contains passwords)

### Best Practices

1. Use proxies for bulk generation
2. Don't generate too many accounts rapidly
3. Keep generated accounts secure
4. Respect rate limits
5. Use responsibly

## 🤝 Contributing

This is an educational project. Contributions welcome for:
- Improved solving algorithms
- Better proxy rotation
- Enhanced UI/UX
- Bug fixes

## 📄 License

This project is licensed under GPL-3.0 - see LICENSE file.

## ⚠️ Disclaimer

This software is provided for **educational purposes only**. 

- The authors are **not responsible** for any misuse
- Automated account creation may violate website Terms of Service
- Use at your own risk
- Always respect website policies and rate limits

## 🎓 How FunCaptcha Works

FunCaptcha (ArkoseLabs) presents interactive challenges:

1. **Rotation Challenges** - Rotate image to correct orientation
2. **Selection Challenges** - Select images matching criteria
3. **Matching Challenges** - Match similar objects

This solver uses API-based patterns to solve these quickly without browser automation.

## 🚀 Comparison with Other Methods

| Feature | This Tool | Selenium-Based | Manual |
|---------|-----------|----------------|--------|
| Speed | ⚡ Ultra-Fast (< 3s) | 🐌 Slow (30-60s) | 🐌 Very Slow |
| Resource Usage | ✅ Low | ❌ High | ❌ N/A |
| Success Rate | 🎯 High | 🎯 Medium | ✅ 100% |
| Automation | ✅ Full | ⚠️ Partial | ❌ None |
| Proxy Support | ✅ Yes | ✅ Yes | ❌ No |

## 📞 Support

For issues:
1. Check this README
2. Verify all requirements are met
3. Try with default settings first
4. Check proxy configuration

---

**Made with ⚡ for fast FunCaptcha solving**

*Similar to funbypass.com - API-based, ultra-fast, no Selenium*
