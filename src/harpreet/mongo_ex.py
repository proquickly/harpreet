# Import the PyMongo library
from pymongo import MongoClient
import pprint
import sys
import time

# Initialize the pretty printer
pp = pprint.PrettyPrinter(indent=4)

# Try to connect to MongoDB with retry logic
max_retries = 3
retry_delay = 2
connection_string = 'mongodb://localhost:27017/'  # Use the port you mapped when starting the container

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt+1}: Connecting to MongoDB at {connection_string}")

        # Connect with a short timeout to fail fast if not available
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)

        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB container!")
        break
    except Exception as e:
        print(f"Connection attempt {attempt+1} failed: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("\nTroubleshooting tips:")
            print("1. Check if your MongoDB container is running: docker ps | grep mongo")
            print("2. Verify port mapping: docker port CONTAINER_ID 27017")
            print("3. Try connecting to the container IP directly")
            print("4. Make sure host firewall allows connections to MongoDB port")
            sys.exit(1)

# Create or access a database
db = client['example_database']

# Create or access a collection (similar to a table in SQL)
collection = db['users']

# ----- INSERT OPERATIONS -----

# Insert a single document
user1 = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "interests": ["programming", "hiking"]
}

result = collection.insert_one(user1)
print(f"Inserted document with ID: {result.inserted_id}")

# Insert multiple documents
users = [
    {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 28,
        "interests": ["reading", "travel"]
    },
    {
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "age": 35,
        "interests": ["cooking", "photography"]
    }
]

result = collection.insert_many(users)
print(f"Inserted documents with IDs: {result.inserted_ids}")

# ----- QUERY OPERATIONS -----

# Find one document
print("\nFinding one user:")
found_user = collection.find_one({"name": "John Doe"})
pp.pprint(found_user)

# Find all documents
print("\nFinding all users:")
all_users = collection.find()
for user in all_users:
    pp.pprint(user)

# Find with query filter
print("\nFinding users over 30:")
older_users = collection.find({"age": {"$gt": 30}})
for user in older_users:
    pp.pprint(user)

# ----- UPDATE OPERATIONS -----

# Update a document
update_result = collection.update_one(
    {"name": "John Doe"},
    {"$set": {"age": 31, "interests": ["programming", "hiking", "chess"]}}
)
print(f"\nModified {update_result.modified_count} document")

# Verify the update
updated_user = collection.find_one({"name": "John Doe"})
print("Updated user:")
pp.pprint(updated_user)

# ----- DELETE OPERATIONS -----

# Delete one document
delete_result = collection.delete_one({"name": "Jane Smith"})
print(f"\nDeleted {delete_result.deleted_count} document")

# Count remaining documents
count = collection.count_documents({})
print(f"Remaining documents: {count}")

# Close connection
client.close()
