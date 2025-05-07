import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
import os

class DestinyInventoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Destiny Inventory Manager")
        self.root.geometry("1200x800")
        
        # Initialize data storage
        self.data_file = Path("inventory_data.json")
        self.inventory_data = self.load_data()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
    def create_sidebar(self):
        sidebar = ttk.Frame(self.main_container, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Character selection
        ttk.Label(sidebar, text="Characters").pack(pady=(0, 5))
        self.character_listbox = tk.Listbox(sidebar, height=3)
        self.character_listbox.pack(fill=tk.X, pady=(0, 10))
        self.character_listbox.insert(0, "Character 1", "Character 2", "Character 3")
        
        # Item type filter
        ttk.Label(sidebar, text="Item Type").pack(pady=(0, 5))
        self.item_type_var = tk.StringVar(value="All")
        item_types = ["All", "Weapons", "Armor", "Ghosts", "Ships", "Sparrows"]
        for item_type in item_types:
            ttk.Radiobutton(sidebar, text=item_type, variable=self.item_type_var, 
                           value=item_type).pack(anchor=tk.W)
        
    def create_main_content(self):
        content = ttk.Frame(self.main_container)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Search bar
        search_frame = ttk.Frame(content)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Inventory display
        self.inventory_tree = ttk.Treeview(content, columns=("Name", "Type", "Power", "Location"),
                                          show="headings")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Type", text="Type")
        self.inventory_tree.heading("Power", text="Power")
        self.inventory_tree.heading("Location", text="Location")
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add some sample data
        sample_items = [
            ("Fatebringer", "Weapon", "1600", "Character 1"),
            ("Lion Rampant", "Armor", "1590", "Character 2"),
            ("Sparrow", "Vehicle", "1600", "Vault")
        ]
        for item in sample_items:
            self.inventory_tree.insert("", tk.END, values=item)
    
    def load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"characters": [], "items": []}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.inventory_data, f, indent=4)

def main():
    root = tk.Tk()
    app = DestinyInventoryManager(root)
    root.mainloop()

if __name__ == "__main__":
    main() 