# EXIF Metadata Editor

A simple GUI tool for embedding metadata into PNG images using ExifTool.

## Features

- **Clean GUI Interface** - Easy-to-use graphical interface
- **PNG Image Support** - Specifically designed for PNG files
- **Multiple Metadata Tags** - Embed data into various EXIF tags:
  - ImageDescription
  - Comment
  - UserComment
  - Copyright
  - Artist
  - Software
- **Automatic Backup** - Creates backup before modifying images
- **ExifTool Integration** - Uses ExifTool for reliable metadata embedding

## Requirements

- Python 3.7+
- ExifTool (must be installed separately)

## Installation

### Step 1: Install ExifTool

**Windows:**
1. Download ExifTool from https://exiftool.org/
2. Extract the executable
3. Rename `exiftool(-k).exe` to `exiftool.exe`
4. Add to system PATH or place in the same folder as this script

**Linux:**
```bash
sudo apt-get install libimage-exiftool-perl
```

**macOS:**
```bash
brew install exiftool
```

### Step 2: Install Python Dependencies

No additional Python packages required (uses built-in tkinter).

## Usage

### Running the Application

**Windows:**
```bash
python main.py
```

**Linux/macOS:**
```bash
python3 main.py
```

### How to Use

1. **Select PNG Image**
   - Click "Browse..." to select your PNG image
   - Or paste the file path directly

2. **Choose Metadata Tags**
   - Check the boxes for tags you want to modify
   - You can select multiple tags

3. **Enter Metadata Content**
   - Type or paste the content you want to embed
   - The same content will be applied to all selected tags

4. **Embed Metadata**
   - Click "✓ Embed Metadata into Image"
   - Confirm the operation
   - A backup will be created automatically

## Examples

### Embedding a Description

1. Select image: `photo.png`
2. Check: `ImageDescription`
3. Enter: `This is a beautiful sunset photograph`
4. Click embed

### Embedding Copyright Info

1. Select image: `artwork.png`
2. Check: `Copyright`, `Artist`
3. Enter: `© 2024 John Doe. All rights reserved.`
4. Click embed

### Embedding Custom Data

1. Select image: `document.png`
2. Check: `Comment`, `UserComment`
3. Enter: Your custom text or data
4. Click embed

## Features

- ✅ Automatic file backup (creates `.backup` file)
- ✅ Input validation (checks file exists, is PNG, etc.)
- ✅ Status messages and error handling
- ✅ Support for multiline text
- ✅ Dark theme UI
- ✅ Cross-platform compatible

## Troubleshooting

**"ExifTool Not Found" Error:**
- Make sure ExifTool is installed
- Verify it's in your system PATH
- Try running `exiftool -ver` in command prompt/terminal

**"Embedding Failed" Error:**
- Check that the PNG file is valid
- Ensure you have write permissions
- Check the backup file wasn't corrupted

**File Permissions Error:**
- Make sure the PNG file is not read-only
- Close any programs that might have the file open

## Technical Details

The tool uses ExifTool with the following command structure:
```bash
exiftool -overwrite_original -TagName="content" image.png
```

Supported metadata tags are standard EXIF/PNG metadata fields that ExifTool can write.

## License

This tool is provided as-is for educational and personal use.

## Credits

- ExifTool by Phil Harvey (https://exiftool.org/)
- GUI built with Python tkinter
