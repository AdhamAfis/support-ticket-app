from pymongo import MongoClient
from bson.objectid import ObjectId

# Load categories from the external file
def load_categories(filename):
    categories = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.endswith(':'):
                current_category = line[:-1]
                categories[current_category] = []
            else:
                categories[current_category].append(line.strip())
    return categories

# Connect to MongoDB
def connect_mongodb(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# Initialize the categories collection in MongoDB
def initialize_categories(db, categories):
    db.categories.drop()
    for category, issues in categories.items():
        db.categories.insert_one({
            "category": category,
            "issues": issues
        })

# Create a new ticket with reference to its category
def create_ticket(db, category_id, issue_type, description):
    ticket = {
        "category_id": ObjectId(category_id),
        "issue_type": issue_type,
        "description": description,
        "status": "Open"
    }
    db.tickets.insert_one(ticket)
    return ticket

# Update ticket status with choices
def update_ticket_status(db, ticket_id):
    status_options = ["Open", "Pending", "Closed"]
    print("Choose new status:")
    for idx, status in enumerate(status_options, 1):
        print(f"{idx}. {status}")
    choice = int(input("Enter the number of the new status: "))
    if 1 <= choice <= len(status_options):
        new_status = status_options[choice - 1]
        db.tickets.update_one({"_id": ObjectId(ticket_id)}, {"$set": {"status": new_status}})
        print("Ticket status updated.")
    else:
        print("Invalid choice. Status not updated.")

# View all tickets with category details
def view_tickets(db):
    tickets = db.tickets.find()
    for ticket in tickets:
        category = db.categories.find_one({"_id": ticket['category_id']})
        if category:
            print_ticket(ticket, category['category'])
        else:
            print("Error: Category not found for ticket:")
            print_ticket(ticket, "Unknown Category")

# Print ticket details
def print_ticket(ticket, category_name):
    print(f"Ticket ID: {ticket['_id']}")
    print(f"Category: {category_name}")
    print(f"Issue Type: {ticket['issue_type']}")
    print(f"Description: {ticket['description']}")
    print(f"Status: {ticket['status']}")
    print("-" * 40)

# Search tickets by category
def search_tickets_by_category(db, category_name):
    category = db.categories.find_one({"category": category_name})
    if category:
        tickets = db.tickets.find({"category_id": category['_id']})
        for ticket in tickets:
            print_ticket(ticket, category_name)
    else:
        print("Category not found.")

# Search tickets by status
def search_tickets_by_status(db, status):
    tickets = db.tickets.find({"status": status})
    for ticket in tickets:
        category = db.categories.find_one({"_id": ticket['category_id']})
        if category:
            print_ticket(ticket, category['category'])
        else:
            print_ticket(ticket, "Unknown Category")

# Display categories and let user choose one
def choose_category(db):
    categories = db.categories.find()
    category_list = []
    print("Available categories:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category['category']}")
        category_list.append(category)
    choice = int(input("Enter the number of the chosen category: "))
    return category_list[choice - 1]

# Display issues for the chosen category and let user choose one
def choose_issue_type(category):
    issues = category['issues']
    print(f"Available issue types for {category['category']}:")
    for idx, issue in enumerate(issues):
        print(f"{idx + 1}. {issue}")
    choice = int(input("Enter the number of the chosen issue type: "))
    return issues[choice - 1]

# Clean up orphaned tickets
def cleanup_orphaned_tickets(db):
    tickets = db.tickets.find()
    for ticket in tickets:
        category = db.categories.find_one({"_id": ticket['category_id']})
        if not category:
            db.tickets.delete_one({"_id": ticket['_id']})
            print(f"Deleted orphaned ticket ID: {ticket['_id']}")

# Main function
def main():
    # Load categories from file
    categories = load_categories('categories.txt')
    
    # Connect to MongoDB
    db = connect_mongodb('mongodb://localhost:27017/', 'support_ticketing_system')

    # Initialize categories collection
    initialize_categories(db, categories)

    # Clean up orphaned tickets
    cleanup_orphaned_tickets(db)

    while True:
        print("1. Create a new ticket")
        print("2. View all tickets")
        print("3. Update ticket status")
        print("4. Search tickets by category")
        print("5. Search tickets by status")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            category = choose_category(db)
            issue_type = choose_issue_type(category)
            description = input("Enter description: ")
            ticket = create_ticket(db, category['_id'], issue_type, description)
            print(f"Ticket created with ID: {ticket['_id']}")
        elif choice == '2':
            view_tickets(db)
        elif choice == '3':
            ticket_id = input("Enter ticket ID: ")
            update_ticket_status(db, ticket_id)
        elif choice == '4':
            category_name = input("Enter category: ")
            search_tickets_by_category(db, category_name)
        elif choice == '5':
            status = input("Enter status (Open, Pending, Closed): ")
            search_tickets_by_status(db, status)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
