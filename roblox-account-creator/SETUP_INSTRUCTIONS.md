# How to Use This Standalone Package

## Option 1: Quick Start (Windows)

1. **Extract** this folder to your desired location
2. **Double-click** `run.bat`
3. The launcher will:
   - Check for Python
   - Install dependencies automatically
   - Start the account generator
4. **Enter** the number of accounts you want to generate
5. **Wait** for completion
6. **Check** `accounts.txt` for your generated accounts

## Option 2: Manual Installation (All Platforms)

### Step 1: Install Python
- Download Python 3.7 or higher from [python.org](https://python.org)
- During installation, **check "Add Python to PATH"**

### Step 2: Install Dependencies
Open terminal/command prompt in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 3: Configure (Optional)
- Edit `config.json` to adjust threads, delays, etc.
- Add proxies to `proxies.txt` (one per line)

### Step 4: Run
```bash
python main.py
```

## Configuration Guide

### config.json
```json
{
  "threads": 5,          // How many accounts to create at once
  "delay": 3,            // Seconds between account creations
  "use_proxies": true,   // Use proxies from proxies.txt
  "debug": false         // Show detailed error messages
}
```

### proxies.txt
Add one proxy per line:
```
http://123.456.789.0:8080
******proxy.example.com:3128
socks5://another-proxy.com:1080
```

## Folder Organization

You can move this entire `roblox-account-creator` folder anywhere you want. Just keep all files together in the same folder.

## Creating a New Repository (Optional)

If you want to put this in a new GitHub repository:

1. **Create a new repo** on GitHub:
   - Go to github.com
   - Click "New repository"
   - Name it (e.g., "roblox-account-creator")
   - Don't initialize with README

2. **Upload files**:
   ```bash
   cd roblox-account-creator
   git init
   git add .
   git commit -m "Initial commit: Roblox account creator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/roblox-account-creator.git
   git push -u origin main
   ```

3. **Done!** Your standalone repo is ready.

## What's Different From Main Repo

This standalone package contains **only** the account creator files. The original repository also includes a web proxy (Doge Unblocker). This package is purely for account generation.

## Support

For issues:
1. Check `STANDALONE_README.md` (main documentation)
2. Check `FUNCAPTCHA_README.md` (technical details)
3. Verify Python and dependencies are installed
4. Check `config.json` settings
5. Review error messages in the console

## File Checklist

Make sure you have all these files:
- [x] run.bat (launcher)
- [x] main.py (entry point)
- [x] generate.py
- [x] generate_counter.py
- [x] util.py
- [x] roblox_signup.py
- [x] funcaptcha_solver.py
- [x] funcaptcha_utils.py
- [x] gui.py
- [x] main_ui.py
- [x] example.py
- [x] config.json
- [x] proxies.txt
- [x] requirements.txt
- [x] README.md (main readme)
- [x] STANDALONE_README.md (this file)
- [x] FUNCAPTCHA_README.md
- [x] SETUP_INSTRUCTIONS.md

If any files are missing, you can re-extract the package or get them from the original repository.

---

**Ready to generate accounts? Run `run.bat` and get started!**
