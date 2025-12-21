"""
EXIF Metadata Editor - GUI Tool for PNG Images
Embeds custom metadata into PNG images using ExifTool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
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
        try:
            result = subprocess.run(['exiftool', '-ver'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.update_status(f"ExifTool v{version} detected")
                return True
            else:
                self.show_exiftool_error()
                return False
        except FileNotFoundError:
            self.show_exiftool_error()
            return False
        except Exception as e:
            self.update_status(f"Error checking ExifTool: {e}")
            return False
    
    def show_exiftool_error(self):
        """Show error when ExifTool is not found"""
        messagebox.showerror(
            "ExifTool Not Found",
            "ExifTool is not installed or not in PATH.\n\n"
            "Please install ExifTool:\n"
            "1. Download from: https://exiftool.org/\n"
            "2. Extract and add to system PATH\n"
            "3. Restart this application"
        )
        self.update_status("ERROR: ExifTool not found")
    
    def embed_metadata(self):
        """Embed metadata into the selected image"""
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
        cmd = ['exiftool']
        
        # Add overwrite flag (no backup)
        cmd.append('-overwrite_original')
        
        # Add each selected tag with the metadata content
        for tag in selected_tags:
            cmd.append(f'-{tag}={metadata_content}')
        
        # Add the image path
        cmd.append(image_path)
        
        # Execute ExifTool
        try:
            self.update_status("Embedding metadata...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
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
            messagebox.showerror("Timeout", "ExifTool operation timed out.")
            self.update_status("✗ Operation timed out")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
            self.update_status(f"✗ Error: {e}")
    
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
