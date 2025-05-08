import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import os
from notion_integration import NotionManager

class DestinyInventoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Destiny Inventory Manager")
        self.root.geometry("1200x800")
        
        # Initialize Notion integration
        self.notion_manager = NotionManager()
        
        # Initialize data storage
        self.data_file = Path("inventory_data.json")
        self.inventory_data = self.load_data()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create menu bar
        self.create_menu()
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Load initial data from Notion
        self.load_notion_data()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Sync with Notion", command=self.sync_with_notion)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Create Notion Database", command=self.create_notion_database)
        
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
                           value=item_type, command=self.filter_items).pack(anchor=tk.W)
        
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
        search_entry.bind('<KeyRelease>', lambda e: self.filter_items())
        
        # Inventory display
        self.inventory_tree = ttk.Treeview(content, columns=("Name", "Type", "Power", "Location", "Notes"),
                                          show="headings")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Type", text="Type")
        self.inventory_tree.heading("Power", text="Power")
        self.inventory_tree.heading("Location", text="Location")
        self.inventory_tree.heading("Notes", text="Notes")
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add right-click menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_item)
        self.context_menu.add_command(label="Delete", command=self.delete_item)
        self.inventory_tree.bind("<Button-3>", self.show_context_menu)
        
    def load_notion_data(self):
        """Load data from Notion and update the tree view"""
        items = self.notion_manager.get_all_items()
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        for item in items:
            self.inventory_tree.insert("", tk.END, values=(
                item["name"],
                item["type"],
                item["power"],
                item["location"],
                item["notes"]
            ))
    
    def sync_with_notion(self):
        """Sync local data with Notion"""
        try:
            self.load_notion_data()
            messagebox.showinfo("Success", "Data synchronized with Notion successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sync with Notion: {str(e)}")
    
    def create_notion_database(self):
        """Create a new Notion database"""
        try:
            database_id = self.notion_manager.create_inventory_database()
            if database_id:
                messagebox.showinfo("Success", "Notion database created successfully!")
            else:
                messagebox.showerror("Error", "Failed to create Notion database")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Notion database: {str(e)}")
    
    def filter_items(self):
        """Filter items based on search text and selected type"""
        search_text = self.search_var.get().lower()
        selected_type = self.item_type_var.get()
        
        for item in self.inventory_tree.get_children():
            values = self.inventory_tree.item(item)["values"]
            name = values[0].lower()
            item_type = values[1]
            
            type_match = selected_type == "All" or item_type == selected_type
            text_match = search_text in name
            
            if type_match and text_match:
                self.inventory_tree.item(item, tags=())
            else:
                self.inventory_tree.item(item, tags=("hidden",))
        
        self.inventory_tree.tag_configure("hidden", hide=True)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.inventory_tree.identify_row(event.y)
        if item:
            self.inventory_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_item(self):
        """Edit selected item"""
        selected = self.inventory_tree.selection()
        if not selected:
            return
        
        item = self.inventory_tree.item(selected[0])
        values = item["values"]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Item")
        dialog.geometry("300x200")
        
        # Add entry fields
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_var = tk.StringVar(value=values[0])
        ttk.Entry(dialog, textvariable=name_var).pack()
        
        ttk.Label(dialog, text="Type:").pack(pady=5)
        type_var = tk.StringVar(value=values[1])
        ttk.Combobox(dialog, textvariable=type_var, 
                    values=["Weapon", "Armor", "Ghost", "Ship", "Sparrow"]).pack()
        
        ttk.Label(dialog, text="Power:").pack(pady=5)
        power_var = tk.StringVar(value=values[2])
        ttk.Entry(dialog, textvariable=power_var).pack()
        
        ttk.Label(dialog, text="Location:").pack(pady=5)
        location_var = tk.StringVar(value=values[3])
        ttk.Combobox(dialog, textvariable=location_var,
                    values=["Character 1", "Character 2", "Character 3", "Vault"]).pack()
        
        def save_changes():
            item_data = {
                "name": name_var.get(),
                "type": type_var.get(),
                "power": power_var.get(),
                "location": location_var.get(),
                "notes": values[4] if len(values) > 4 else ""
            }
            # Update in Notion
            self.notion_manager.update_item(selected[0], item_data)
            # Refresh display
            self.load_notion_data()
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_changes).pack(pady=10)
    
    def delete_item(self):
        """Delete selected item"""
        selected = self.inventory_tree.selection()
        if not selected:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            # Delete from Notion
            self.notion_manager.delete_item(selected[0])
            # Refresh display
            self.load_notion_data()
    
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