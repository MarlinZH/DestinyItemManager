from notion_client import Client
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

class NotionManager:
    def __init__(self):
        load_dotenv()
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        
    def create_inventory_database(self) -> str:
        """Create a new database in Notion for inventory items"""
        try:
            response = self.notion.databases.create(
                parent={"type": "page_id", "page_id": os.getenv("NOTION_PAGE_ID")},
                title=[{"type": "text", "text": {"content": "Destiny Inventory"}}],
                properties={
                    "Name": {"title": {}},
                    "Type": {"select": {
                        "options": [
                            {"name": "Weapon", "color": "red"},
                            {"name": "Armor", "color": "blue"},
                            {"name": "Ghost", "color": "green"},
                            {"name": "Ship", "color": "purple"},
                            {"name": "Sparrow", "color": "orange"}
                        ]
                    }},
                    "Power": {"number": {}},
                    "Location": {"select": {
                        "options": [
                            {"name": "Character 1", "color": "default"},
                            {"name": "Character 2", "color": "default"},
                            {"name": "Character 3", "color": "default"},
                            {"name": "Vault", "color": "default"}
                        ]
                    }},
                    "Notes": {"rich_text": {}}
                }
            )
            return response["id"]
        except Exception as e:
            print(f"Error creating database: {e}")
            return None

    def add_item(self, item_data: Dict) -> Optional[str]:
        """Add a new item to the Notion database"""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Name": {"title": [{"text": {"content": item_data["name"]}}]},
                    "Type": {"select": {"name": item_data["type"]}},
                    "Power": {"number": int(item_data["power"])},
                    "Location": {"select": {"name": item_data["location"]}},
                    "Notes": {"rich_text": [{"text": {"content": item_data.get("notes", "")}}]}
                }
            )
            return response["id"]
        except Exception as e:
            print(f"Error adding item: {e}")
            return None

    def get_all_items(self) -> List[Dict]:
        """Retrieve all items from the Notion database"""
        try:
            response = self.notion.databases.query(
                database_id=self.database_id,
                sorts=[{"property": "Name", "direction": "ascending"}]
            )
            
            items = []
            for page in response["results"]:
                props = page["properties"]
                item = {
                    "id": page["id"],
                    "name": props["Name"]["title"][0]["text"]["content"],
                    "type": props["Type"]["select"]["name"],
                    "power": props["Power"]["number"],
                    "location": props["Location"]["select"]["name"],
                    "notes": props["Notes"]["rich_text"][0]["text"]["content"] if props["Notes"]["rich_text"] else ""
                }
                items.append(item)
            return items
        except Exception as e:
            print(f"Error retrieving items: {e}")
            return []

    def update_item(self, item_id: str, item_data: Dict) -> bool:
        """Update an existing item in the Notion database"""
        try:
            self.notion.pages.update(
                page_id=item_id,
                properties={
                    "Name": {"title": [{"text": {"content": item_data["name"]}}]},
                    "Type": {"select": {"name": item_data["type"]}},
                    "Power": {"number": int(item_data["power"])},
                    "Location": {"select": {"name": item_data["location"]}},
                    "Notes": {"rich_text": [{"text": {"content": item_data.get("notes", "")}}]}
                }
            )
            return True
        except Exception as e:
            print(f"Error updating item: {e}")
            return False

    def delete_item(self, item_id: str) -> bool:
        """Delete an item from the Notion database"""
        try:
            self.notion.pages.update(
                page_id=item_id,
                archived=True
            )
            return True
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False 