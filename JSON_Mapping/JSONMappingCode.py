import pymongo
from bson import json_util
import json

# MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'NewJsonTesting'
json_table_name = 'jsonTable'

# Connect to MongoDB
client = pymongo.MongoClient(mongo_host, mongo_port)
db = client[database_name]
json_collection = db[json_table_name]

# Fetch BSON document containing JSON data
bson_document = json_collection.find_one({})

# Convert BSON to JSON
json_data = json_util.loads(json_util.dumps(bson_document))

# Specify the target value to check
target_value = 'photo_1@05-09-2022_11-54-38'

# List to store the matching blocks
matching_blocks = []

# Recursive function to search for the target value within the JSON data
def search_target_value(data):
    if isinstance(data, dict):
        # print('Data:', data)
        if 'photo' in data and data['photo'] == 'photos/'+target_value+'.jpg':
            matching_blocks.append(data)
        for key, value in data.items():
            # print(f"Key: {key}, Value: {value}")
            search_target_value(value)
    elif isinstance(data, list):
        for item in data:
            search_target_value(item)

# Start the recursive search within the 'messages' field
search_target_value(json_data)

# Print the matching blocks
if matching_blocks:
    print(f"Matching blocks for the target value {target_value}:")
    for block in matching_blocks:
        print(json.dumps(block, indent=2))
else:
    print(f"No matching blocks found for the target value {target_value}.")
