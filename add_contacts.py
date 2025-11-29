"""
Script to add contacts to the AI Moses database
"""
from src.database import Database

# Initialize database
db = Database()

# Define your contacts here
# Format: (phone_number, name, relationship, tone, topics)
contacts = [
    ("+1234567890", "Mom", "family", "warm", "family, health, cooking"),
    ("+0987654321", "Dad", "family", "casual", "work, sports, news"),
    ("+1122334455", "Sarah", "friend", "friendly", "movies, travel, coffee"),
    ("+5566778899", "Boss", "work", "professional", "projects, deadlines, meetings"),
    # Add more contacts below in the same format:
    # ("+1234567890", "Name", "relationship", "tone", "topics"),
]

def add_all_contacts():
    """Add all contacts to the database"""
    print("Adding contacts to database...\n")
    
    for phone, name, relationship, tone, topics in contacts:
        success = db.add_caller_profile(
            phone_number=phone,
            name=name,
            relationship=relationship,
            tone=tone,
            topics=topics
        )
        
        if success:
            print(f"✅ Added: {name} ({phone}) - {relationship}")
        else:
            print(f"❌ Failed to add: {name}")
    
    print(f"\n✨ Done! Added {len(contacts)} contacts.")
    print("You can view them on the dashboard at http://localhost:5000")

if __name__ == "__main__":
    add_all_contacts()
