import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from PyPDF2 import PdfMerger
import threading

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Pro")
        self.root.geometry("700x500")
        self.root.minsize(600, 450)
        
        # Set theme colors
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2980b9"  # Darker blue
        self.bg_color = "#f5f5f5"  # Light gray
        self.accent_color = "#e74c3c"  # Red for remove/clear
        self.success_color = "#2ecc71"  # Green for merge
        
        self.root.configure(bg=self.bg_color)
        
        # PDF files list
        self.pdf_files = []
        
        # Create custom style
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("Primary.TButton", background=self.primary_color)
        self.style.configure("Accent.TButton", background=self.accent_color)
        self.style.configure("Success.TButton", background=self.success_color)
        
        # Create UI elements
        self.create_header()
        self.create_file_list()
        self.create_buttons()
        self.create_status_bar()
        
    def create_header(self):
        """Create the header section with logo and title"""
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame, 
            text="PDF Merger Pro",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Combine multiple PDFs easily",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#555555"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(10, 0))
    
    def create_file_list(self):
        """Create the file listbox with scrollbar"""
        list_frame = ttk.Frame(self.root, style="TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File count label
        self.file_count_var = tk.StringVar()
        self.file_count_var.set("PDF Files: 0")
        file_count_label = tk.Label(
            list_frame,
            textvariable=self.file_count_var,
            font=("Arial", 10),
            anchor="w",
            bg=self.bg_color
        )
        file_count_label.pack(fill=tk.X, pady=(0, 5))
        
        # Create a frame with border
        listbox_container = tk.Frame(
            list_frame,
            bd=1,
            relief=tk.SOLID,
            bg="#ffffff"
        )
        listbox_container.pack(fill=tk.BOTH, expand=True)
        
        # Listbox with custom colors and font
        self.listbox = tk.Listbox(
            listbox_container,
            selectmode=tk.EXTENDED,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#333333",
            selectbackground=self.primary_color,
            selectforeground="#ffffff",
            activestyle="none",
            highlightthickness=0,
            bd=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(listbox_container, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
    def create_buttons(self):
        """Create action buttons"""
        btn_frame = ttk.Frame(self.root, style="TFrame")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # First row of buttons
        action_frame = ttk.Frame(btn_frame, style="TFrame")
        action_frame.pack(fill=tk.X)
        
        # Add button with custom styling
        self.add_btn = tk.Button(
            action_frame,
            text="Add PDFs",
            command=self.add_files,
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="#ffffff",
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2",
            activebackground=self.secondary_color,
            activeforeground="#ffffff"
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove button
        self.remove_btn = tk.Button(
            action_frame,
            text="Remove Selected",
            command=self.remove_selected,
            font=("Arial", 10, "bold"),
            bg=self.accent_color,
            fg="#ffffff",
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="#ffffff"
        )
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_btn = tk.Button(
            action_frame,
            text="Clear All",
            command=self.clear_list,
            font=("Arial", 10, "bold"),
            bg="#7f8c8d",
            fg="#ffffff",
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2",
            activebackground="#626567",
            activeforeground="#ffffff"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Move buttons
        move_frame = ttk.Frame(btn_frame, style="TFrame")
        move_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Move up button
        self.move_up_btn = tk.Button(
            move_frame,
            text="Move Up",
            command=self.move_up,
            font=("Arial", 10),
            bg="#95a5a6",
            fg="#ffffff",
            padx=15,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        self.move_up_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Move down button
        self.move_down_btn = tk.Button(
            move_frame,
            text="Move Down",
            command=self.move_down,
            font=("Arial", 10),
            bg="#95a5a6",
            fg="#ffffff",
            padx=15,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        self.move_down_btn.pack(side=tk.LEFT)
        
        # Merge button at the bottom
        merge_frame = ttk.Frame(self.root, style="TFrame")
        merge_frame.pack(fill=tk.X, padx=20, pady=(5, 20))
        
        self.merge_btn = tk.Button(
            merge_frame,
            text="MERGE PDFs",
            command=self.merge_files,
            font=("Arial", 12, "bold"),
            bg=self.success_color,
            fg="#ffffff",
            padx=20,
            pady=10,
            bd=0,
            cursor="hand2",
            activebackground="#27ae60",
            activeforeground="#ffffff"
        )
        self.merge_btn.pack(fill=tk.X)
        
    def create_status_bar(self):
        """Create status bar at the bottom"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 9),
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#ecf0f1",
            padx=10,
            pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def add_files(self):
        """Add PDF files to the list"""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    # Display only the filename, not the full path
                    filename = os.path.basename(file)
                    self.listbox.insert(tk.END, f"{filename} ({os.path.dirname(file)})")
            
            self.update_file_count()
            self.status_var.set(f"Added {len(files)} file(s)")
    
    def remove_selected(self):
        """Remove selected files from the list"""
        selected_indices = self.listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("Info", "No files selected")
            return
            
        for index in reversed(selected_indices):
            self.pdf_files.pop(index)
            self.listbox.delete(index)
            
        self.update_file_count()
        self.status_var.set(f"Removed {len(selected_indices)} file(s)")
        
    def clear_list(self):
        """Clear all files from the list"""
        if not self.pdf_files:
            return
            
        self.pdf_files.clear()
        self.listbox.delete(0, tk.END)
        self.update_file_count()
        self.status_var.set("All files cleared")
        
    def move_up(self):
        """Move selected item up in the list"""
        selected_indices = self.listbox.curselection()
        
        if not selected_indices or selected_indices[0] == 0:
            return
            
        index = selected_indices[0]
        # Swap in pdf_files list
        self.pdf_files[index], self.pdf_files[index-1] = self.pdf_files[index-1], self.pdf_files[index]
        
        # Update listbox
        text = self.listbox.get(index)
        self.listbox.delete(index)
        self.listbox.insert(index-1, text)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index-1)
        self.listbox.see(index-1)
        
    def move_down(self):
        """Move selected item down in the list"""
        selected_indices = self.listbox.curselection()
        
        if not selected_indices or selected_indices[0] == len(self.pdf_files) - 1:
            return
            
        index = selected_indices[0]
        # Swap in pdf_files list
        self.pdf_files[index], self.pdf_files[index+1] = self.pdf_files[index+1], self.pdf_files[index]
        
        # Update listbox
        text = self.listbox.get(index)
        self.listbox.delete(index)
        self.listbox.insert(index+1, text)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index+1)
        self.listbox.see(index+1)
    
    def update_file_count(self):
        """Update the file count label"""
        count = len(self.pdf_files)
        self.file_count_var.set(f"PDF Files: {count}")
        
    def merge_files(self):
        """Merge PDF files"""
        if len(self.pdf_files) < 2:
            messagebox.showerror("Error", "Please add at least two PDF files to merge")
            return
            
        output_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not output_path:
            return
            
        # Start merging in a separate thread to prevent UI freezing
        self.status_var.set("Merging files... Please wait")
        self.merge_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._perform_merge, args=(output_path,))
        thread.daemon = True
        thread.start()
    
    def _perform_merge(self, output_path):
        """Perform the actual PDF merging in a separate thread"""
        try:
            merger = PdfMerger()
            
            for file in self.pdf_files:
                merger.append(file)
                
            merger.write(output_path)
            merger.close()
            
            # Schedule UI updates to run on the main thread
            self.root.after(0, lambda: self._merge_complete(output_path))
            
        except Exception as e:
            # Schedule error message to run on the main thread
            self.root.after(0, lambda: self._merge_error(str(e)))
    
    def _merge_complete(self, output_path):
        """Handle successful merge completion"""
        self.merge_btn.config(state=tk.NORMAL)
        self.status_var.set("Merge completed successfully")
        
        result = messagebox.askquestion(
            "Success",
            f"Merged PDF saved as:\n{output_path}\n\nWould you like to clear the file list?",
            icon="info"
        )
        
        if result == "yes":
            self.clear_list()
    
    def _merge_error(self, error_msg):
        """Handle merge errors"""
        self.merge_btn.config(state=tk.NORMAL)
        self.status_var.set("Error during merge")
        messagebox.showerror("Error", f"Failed to merge PDFs:\n{error_msg}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()