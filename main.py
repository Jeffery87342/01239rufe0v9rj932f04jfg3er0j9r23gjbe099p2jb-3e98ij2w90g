"""
EXIF Metadata Editor - GUI Tool for PNG Images
Embeds custom metadata into PNG images using ExifTool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import json
from pathlib import Path


class ExifMetadataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("EXIF Metadata Editor")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.image_path = tk.StringVar()
        self.selected_tags = []
        self.metadata_text = tk.StringVar()
        self.exiftool_cmd = 'exiftool'  # Will be set by check_exiftool()
        self.config_file = Path.home() / '.exif_metadata_editor_config.json'
        
        # Build UI
        self.build_ui()
        
        # Check for ExifTool
        self.check_exiftool()
    
    def setup_styles(self):
        """Configure UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        accent_color = "#0d7377"
        
        self.root.configure(bg=bg_color)
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=accent_color)
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Success.TButton", background="#28a745", foreground="white")
        
    def build_ui(self):
        """Build the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="EXIF Metadata Editor", style="Title.TLabel")
        title.pack(pady=(0, 20))
        
        # Step 1: Image Path Selection
        self.create_image_selection_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Step 2: Tag Selection
        self.create_tag_selection_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Step 3: Metadata Input
        self.create_metadata_input_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Step 4: Embed Button
        self.create_embed_section(main_frame)
        
        # Status Bar
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="#888888")
        self.status_label.pack(side=tk.BOTTOM, pady=(10, 0))
    
    def create_image_selection_section(self, parent):
        """Create image path selection section"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=5)
        
        label = ttk.Label(section_frame, text="Step 1: Select PNG Image", font=("Segoe UI", 11, "bold"))
        label.pack(anchor=tk.W, pady=(0, 10))
        
        path_frame = ttk.Frame(section_frame)
        path_frame.pack(fill=tk.X)
        
        entry = ttk.Entry(path_frame, textvariable=self.image_path, font=("Segoe UI", 10))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="Browse...", command=self.browse_image)
        browse_btn.pack(side=tk.LEFT)
    
    def create_tag_selection_section(self, parent):
        """Create metadata tag selection section"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=5)
        
        label = ttk.Label(section_frame, text="Step 2: Select Metadata Tags", font=("Segoe UI", 11, "bold"))
        label.pack(anchor=tk.W, pady=(0, 10))
        
        info_label = ttk.Label(section_frame, text="Choose which metadata tags to modify:", foreground="#888888")
        info_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Tags frame with checkboxes
        tags_frame = ttk.Frame(section_frame)
        tags_frame.pack(fill=tk.X, pady=5)
        
        # Define available tags
        self.tag_vars = {}
        tags = [
            ("ImageDescription", "General description of the image"),
            ("Comment", "User comment field"),
            ("UserComment", "EXIF user comment"),
            ("Copyright", "Copyright information"),
            ("Artist", "Creator/artist name"),
            ("Software", "Software used to create image")
        ]
        
        for i, (tag, description) in enumerate(tags):
            var = tk.BooleanVar()
            self.tag_vars[tag] = var
            
            cb = ttk.Checkbutton(tags_frame, text=f"{tag}", variable=var)
            cb.grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=10, pady=3)
            
            desc_label = ttk.Label(tags_frame, text=f"({description})", foreground="#666666", font=("Segoe UI", 8))
            desc_label.grid(row=i//2, column=(i%2)*2+1, sticky=tk.W, padx=5, pady=3)
    
    def create_metadata_input_section(self, parent):
        """Create metadata text input section"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        label = ttk.Label(section_frame, text="Step 3: Enter Metadata Content", font=("Segoe UI", 11, "bold"))
        label.pack(anchor=tk.W, pady=(0, 10))
        
        info_label = ttk.Label(section_frame, text="Paste or type the content to embed:", foreground="#888888")
        info_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(
            section_frame, 
            height=8, 
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def create_embed_section(self, parent):
        """Create embed button section"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=10)
        
        embed_btn = ttk.Button(
            section_frame, 
            text="✓ Embed Metadata into Image", 
            command=self.embed_metadata,
            style="Success.TButton"
        )
        embed_btn.pack(pady=10)
    
    def browse_image(self):
        """Open file dialog to select PNG image"""
        filename = filedialog.askopenfilename(
            title="Select PNG Image",
            filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            self.image_path.set(filename)
            self.update_status(f"Selected: {os.path.basename(filename)}")
    
    def check_exiftool(self):
        """Check if ExifTool is available"""
        # First, try to load saved custom path
        custom_path = self.load_exiftool_path()
        if custom_path and self.test_exiftool_path(custom_path):
            return True
        
        # Try different command names (exiftool on Linux/Mac, exiftool.exe on Windows)
        commands_to_try = ['exiftool', 'exiftool.exe']
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run([cmd, '-ver'], capture_output=True, text=True, timeout=5, shell=False)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.update_status(f"✓ ExifTool v{version} ready")
                    self.exiftool_cmd = cmd  # Store which command works
                    return True
            except (FileNotFoundError, OSError):
                continue
            except Exception as e:
                print(f"Error checking {cmd}: {e}")
                continue
        
        # If we get here, ExifTool was not found
        self.show_exiftool_error()
        self.exiftool_cmd = 'exiftool'  # Default fallback
        return False
    
    def load_exiftool_path(self):
        """Load saved ExifTool path from config file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('exiftool_path')
        except Exception as e:
            print(f"Error loading config: {e}")
        return None
    
    def save_exiftool_path(self, path):
        """Save ExifTool path to config file"""
        try:
            config = {'exiftool_path': path}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def test_exiftool_path(self, path):
        """Test if the given ExifTool path works"""
        try:
            result = subprocess.run([path, '-ver'], capture_output=True, text=True, timeout=5, shell=False)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.update_status(f"✓ ExifTool v{version} ready (custom path)")
                self.exiftool_cmd = path
                return True
        except Exception as e:
            print(f"Error testing path {path}: {e}")
        return False
    
    def show_exiftool_error(self):
        """Show error when ExifTool is not found"""
        # Ask user if they want to locate ExifTool manually
        response = messagebox.askyesno(
            "ExifTool Not Found",
            "ExifTool is not installed or not found in system PATH.\n\n"
            "Do you want to locate exiftool.exe manually?\n\n"
            "Click 'Yes' to browse for exiftool.exe\n"
            "Click 'No' to see installation instructions"
        )
        
        if response:
            # User wants to browse for ExifTool
            file_path = filedialog.askopenfilename(
                title="Locate exiftool.exe",
                filetypes=[("ExifTool Executable", "exiftool.exe"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Test if the selected file is ExifTool
                if self.test_exiftool_path(file_path):
                    # Save the path for future use
                    self.save_exiftool_path(file_path)
                    messagebox.showinfo(
                        "ExifTool Found",
                        f"ExifTool has been located and saved!\n\nPath: {file_path}\n\n"
                        "This path will be used for future sessions."
                    )
                else:
                    messagebox.showerror(
                        "Invalid ExifTool",
                        "The selected file is not a valid ExifTool executable.\n\n"
                        "Please make sure you select exiftool.exe"
                    )
                    self.update_status("⚠ ERROR: Invalid ExifTool executable")
            else:
                self.update_status("⚠ ERROR: ExifTool not found")
        else:
            # Show installation instructions
            error_msg = (
                "INSTALLATION INSTRUCTIONS:\n\n"
                "Windows:\n"
                "1. Download exiftool from: https://exiftool.org/\n"
                "2. Extract exiftool(-k).exe and rename to exiftool.exe\n"
                "3. Place in C:\\Windows\\ or add folder to PATH\n"
                "   OR use 'Browse' option when prompted\n\n"
                "Linux:\n"
                "  sudo apt-get install libimage-exiftool-perl\n\n"
                "macOS:\n"
                "  brew install exiftool\n\n"
                "After installation, restart this application."
            )
            messagebox.showinfo("Installation Instructions", error_msg)
            self.update_status("⚠ ERROR: ExifTool not found - See installation instructions")
    
    def embed_metadata(self):
        """Embed metadata into the selected image"""
        # First, check if ExifTool command is available
        if not hasattr(self, 'exiftool_cmd') or not self.exiftool_cmd:
            messagebox.showerror(
                "ExifTool Not Configured",
                "ExifTool path is not configured. Please restart the application and select the ExifTool executable."
            )
            return
        
        # Validate image path
        image_path = self.image_path.get()
        if not image_path:
            messagebox.showwarning("No Image", "Please select a PNG image first.")
            return
        
        if not os.path.exists(image_path):
            messagebox.showerror("File Not Found", f"The file does not exist:\n{image_path}")
            return
        
        if not image_path.lower().endswith('.png'):
            messagebox.showwarning("Invalid Format", "Please select a PNG image file.")
            return
        
        # Get selected tags
        selected_tags = [tag for tag, var in self.tag_vars.items() if var.get()]
        if not selected_tags:
            messagebox.showwarning("No Tags Selected", "Please select at least one metadata tag to modify.")
            return
        
        # Get metadata text
        metadata_content = self.text_area.get("1.0", tk.END).strip()
        if not metadata_content:
            messagebox.showwarning("No Content", "Please enter the metadata content to embed.")
            return
        
        # Confirm action
        confirm_msg = f"Embed metadata into:\n{os.path.basename(image_path)}\n\n"
        confirm_msg += f"Tags: {', '.join(selected_tags)}\n\n"
        confirm_msg += "This will modify the original file. Continue?"
        
        if not messagebox.askyesno("Confirm Embedding", confirm_msg):
            return
        
        # Create backup
        backup_path = image_path + ".backup"
        try:
            import shutil
            shutil.copy2(image_path, backup_path)
            self.update_status("Backup created...")
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Could not create backup:\n{e}")
            return
        
        # Build ExifTool command
        cmd = [self.exiftool_cmd]
        
        # Add overwrite flag (no backup)
        cmd.append('-overwrite_original')
        
        # For long metadata content, write to a temporary file to avoid Windows command-line length limits
        # Windows has a ~8191 character limit for command lines
        temp_file = None
        try:
            # Create temporary file for metadata content
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8')
            temp_file.write(metadata_content)
            temp_file.close()
            
            # Add each selected tag using file input syntax (-TAG<=FILE)
            # This avoids command-line length limitations
            for tag in selected_tags:
                cmd.append(f'-{tag}<={temp_file.name}')
            
            # Add the image path
            cmd.append(image_path)
            
            # Execute ExifTool
            self.update_status("Embedding metadata...")
            
            # Debug: print command being executed
            print(f"Executing command: {cmd}")
            print(f"ExifTool path: {self.exiftool_cmd}")
            print(f"Temp file: {temp_file.name}")
            print(f"Content length: {len(metadata_content)} characters")
            
            # Use shell=False for security and proper path handling
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                shell=False
            )
            
            # Clean up temp file after execution
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            
            if result.returncode == 0:
                # Success
                messagebox.showinfo(
                    "Success!",
                    f"Metadata successfully embedded into:\n{os.path.basename(image_path)}\n\n"
                    f"Tags modified: {', '.join(selected_tags)}\n"
                    f"Backup saved as: {os.path.basename(backup_path)}"
                )
                self.update_status("✓ Metadata embedded successfully!")
                
                # Show output details
                if result.stdout:
                    print(f"ExifTool output: {result.stdout}")
            else:
                # Error
                error_msg = result.stderr if result.stderr else "Unknown error"
                messagebox.showerror(
                    "Embedding Failed",
                    f"ExifTool failed to embed metadata:\n\n{error_msg}"
                )
                self.update_status("✗ Embedding failed")
                
                # Restore backup
                try:
                    import shutil
                    shutil.copy2(backup_path, image_path)
                    messagebox.showinfo("Restored", "Original file restored from backup.")
                except:
                    pass
        
        except subprocess.TimeoutExpired:
            # Clean up temp file on timeout
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            messagebox.showerror("Timeout", "ExifTool operation timed out.")
            self.update_status("✗ Operation timed out")
        except FileNotFoundError as e:
            # Clean up temp file on error
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            # This is the WinError 2 - ExifTool executable not found
            error_msg = (
                f"ExifTool executable not found!\n\n"
                f"Command attempted: {self.exiftool_cmd}\n\n"
                f"Error: {e}\n\n"
                f"Please ensure ExifTool is properly installed and the path is correct.\n"
                f"You can browse for exiftool.exe manually by restarting the application."
            )
            messagebox.showerror("ExifTool Not Found", error_msg)
            self.update_status("✗ ExifTool not found")
            print(f"FileNotFoundError: {e}")
            print(f"ExifTool command: {self.exiftool_cmd}")
            print(f"Full command: {cmd}")
        except Exception as e:
            # Clean up temp file on any error
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            messagebox.showerror("Error", f"An error occurred:\n{type(e).__name__}: {e}")
            self.update_status(f"✗ Error: {e}")
            print(f"Exception: {type(e).__name__}: {e}")
            print(f"ExifTool command: {self.exiftool_cmd}")
            print(f"Full command: {cmd}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ExifMetadataEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
