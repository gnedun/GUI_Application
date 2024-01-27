from bson.binary import Binary
from bson import ObjectId
from pymongo import MongoClient
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
from tkinter import ttk  # Import the ttk module
from bson import json_util
import json
from datetime import datetime
import math

# Custom JSON encoder class to handle serialization of ObjectId and datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Recursive function to search for the target value within the JSON data
def search_target_value(data, target_value):
    if isinstance(data, dict):
        if ('photo' in data and data['photo'] == 'photos/' + target_value) or ('thumbnail' in data and data['thumbnail'] == 'video_files/' + target_value):
            return data
        for key, value in data.items():
            result = search_target_value(value, target_value)  # Recursively search within the value
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = search_target_value(item, target_value)  # Recursively search within the item
            if result:
                return result
    return None

# Function to convert JSON data to a string without formatting
def flatten_json(json_data, prefix=''):
    content = []
    for key, value in json_data.items():
        new_key = key if not prefix else f"{prefix}.{key}"
        if isinstance(value, dict):
            content.extend(flatten_json(value, new_key))
        else:
            # Convert lists to a string representation
            if isinstance(value, list):
                value = [str(item).replace('\n', '\n') for item in value]
                value = '\n'.join(value)
            # Convert other data types to string representation
            else:
                value = str(value).replace('\n', '\n')
            content.append(f"{new_key}: {value}")
    return content

# Create a Tkinter window
root = tk.Tk()
root.geometry("1200x600")

# Connect to MongoDB database and retrieve the binary data
client = MongoClient('mongodb://localhost:27017/')
db = client['NewJsonTesting']
collection = db['imageTable']
results = collection.find()

# Create a list to store the individual image file objects and JSON data
image_file_objects = []
json_data_list = []
image_json_mapping = {}

# Fetch BSON document containing JSON data
json_collection = db['jsonTable']
bson_document = json_collection.find_one({})

# Convert BSON to JSON
json_data = json_util.loads(json_util.dumps(bson_document))

# Create a list to store references to the image PhotoImage objects
listbox_images = []  # List to store images displayed in the listbox

# Load the images and JSON data
for i, result in enumerate(results):
    try:
        file_type = result['type']
        if file_type == 'image':
            data = result['data']
            image_data = bytes(data)
            img = Image.open(BytesIO(image_data))
            img = img.resize((200, 150))  # Resize the image to thumbnail size
            image_file_objects.append(img)

            # Find the matching JSON data for the image
            image_name = result['name']
            matching_json_data = search_target_value(json_data, image_name)
            if matching_json_data:
                # Include only specific fields in the JSON data text
                json_data_text = json.dumps({field: value for field, value in matching_json_data.items()
                                             if field in ['id', 'type', 'date', 'from_id', 'photo', 'text']},
                                            indent=2, cls=CustomJSONEncoder)
            else:
                json_data_text = 'No JSON data found'

            json_data_list.append(json_data_text)
            image_json_mapping[image_name] = json_data_text

    except (KeyError, TypeError):
        print("exception")
        continue

# Create a frame for the left side (gallery view)
gallery_frame = tk.Frame(root)
gallery_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a canvas to display the images in the listbox
canvas = tk.Canvas(gallery_frame, width=200, height=150)
canvas.pack()

# Create a scrollbar for the canvas
scrollbar = tk.Scrollbar(gallery_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Connect the scrollbar to the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a treeview widget to show the gallery view of images
treeview = ttk.Treeview(gallery_frame, columns=("name", "image"), selectmode="browse", height=20)
treeview.pack(pady=10)

# ... (rest of the code)

# Add images and names to the treeview
for i, image_obj in enumerate(image_file_objects):
    # Convert the image to PhotoImage and store the reference
    photo = ImageTk.PhotoImage(image_obj)
    listbox_images.append(photo)  # Append the PhotoImage to the list for reference

    # Add the image and name to the treeview as a new item
    treeview.insert("", "end", values=(f"Image {i + 1}", ""), image=photo)  # Add an empty image to display the thumbnail

# Function to show pop-up with image and JSON data
def show_popup(event):
    item = treeview.focus()
    if item:
        image_index = int(item[1:]) - 1
        selected_json_data = json_data_list[image_index]

        # Create a new top-level window for the pop-up
        popup_window = tk.Toplevel(root)

        # Display the selected image in the popup
        image_label = tk.Label(popup_window, image=listbox_images[image_index])  # Use the stored reference
        image_label.pack(pady=10)
        # Convert the JSON data to a flattened string without formatting
        json_text_content = '\n'.join(flatten_json(json.loads(selected_json_data)))

        # Create a Text widget for the JSON data with a border
        json_text = tk.Text(popup_window, wrap=tk.WORD, height=10, width=50, bd=1, relief=tk.SOLID)
        json_text.insert(tk.END, json_text_content)
        json_text.pack(pady=10)

# Bind the click event of the treeview to the show_popup function
treeview.bind("<<TreeviewSelect>>", show_popup)

# Set the scroll region for the canvas to allow scrolling in the treeview
treeview.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Position the images in the canvas
for i, photo in enumerate(listbox_images):
    canvas.create_image(100, i * 160 + 80, image=photo, anchor=tk.CENTER)

# Run the Tkinter event loop
root.mainloop()
