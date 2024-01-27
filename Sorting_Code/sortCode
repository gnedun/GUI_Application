import pymongo
from datetime import datetime
import os
import json
from bson import Binary
from pymongo import MongoClient
from gridfs import GridFS

# Define the path to the collection directory
collection_directory = "C:/Users/gnedu/Documents/GA Work/newTestFiles"

# Get the current time
current_time = datetime.now()

# Define a new client for the collection folder
client = MongoClient("mongodb://localhost:27017/")

# Traverse through all subdirectories within the collection directory
for subdir in next(os.walk(collection_directory))[1]:
    # Create a new collection with the same name as the subdirectory
    db = client[subdir]

    # Define a list of valid file extensions and their types
    valid_extensions = {
        ".html": "html",
        ".jpg": "image",
        ".jpeg": "image",
        ".png": "image",
        ".mp4": "video",
        ".avi": "video",
        ".wmv": "video",
        ".mp3": "audio",
        ".wav": "audio",
        ".json": "json"
    }

    # Define the collections for each file type under the current database
    image_collection = db["imageTable"]
    json_collection = db["jsonTable"]
    video_collection = db["videoTable"]
    html_collection = db["htmlTable"]

    # Traverse through all directories and sub-directories within the subdirectory
    for root, dirs, files in os.walk(os.path.join(collection_directory, subdir)):
        # Traverse through all files in the current directory
        for file in files:
            # Select the files with valid extensions
            if file.lower().endswith(tuple(valid_extensions.keys())):
                file_path = os.path.join(root, file)

                # Check if the file already exists in the database
                existing_file = image_collection.find_one({"name": file.lower()})
                if existing_file is not None:
                    print(f"File {file} already exists in database. Skipping...")
                    continue

                with open(file_path, "rb") as f:
                    file_data = f.read()

                file_extension = os.path.splitext(file)[1]
                file_type = valid_extensions[file_extension.lower()]

                # Load JSON files as Python objects
                if file_type == "json":
                    with open(file_path, encoding='utf-8-sig') as f:
                        file_data = json.load(f)
                    data = {"data": file_data}
                else:
                    data = {"data": Binary(file_data)}

                # Use GridFS to store large files
                if file_type in ["video", "audio"]:
                    if len(file_data) > 16793598:
                        fs = GridFS(db)
                        file_id = fs.put(file_data, filename=file, type=file_type, time=current_time,
                                         content_type="video/mp4")
                        print(f"{file_path} saved successfully with GridFS!")
                        continue

                # Save data to the appropriate collection
                data["name"] = file
                data["type"] = file_type
                data["time"] = current_time

                if file_type == "image":
                    image_collection.insert_one(data)
                    print(f"{file_path} saved successfully in imageTable!")
                elif file_type == "json":
                    json_collection.insert_one(data)
                    print(f"{file_path} saved successfully in jsonTable!")
                elif file_type == "video":
                    video_collection.insert_one(data)
                    print(f"{file_path} saved successfully in videoTable!")
                elif file_type == "html":
                    html_collection.insert_one(data)
                    print(f"{file_path} saved successfully in htmlTable!")
                else:
                    db.insert_one(data)
                    print(f"{file_path} saved successfully in {subdir} collection!")

        # Print a message when all files in the current directory have been saved
        print(f"All files in {root} saved successfully in their respective tables!")

# Close the connection to the MongoDB database for the collection folder
client.close()
