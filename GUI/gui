from bson.binary import Binary
from bson import ObjectId
from pymongo import MongoClient
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO

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


# Rest of the code...

# Connect to MongoDB database and retrieve the binary data
client = MongoClient('mongodb://localhost:27017/')
db = client['NewJsonTesting']
collection = db['imageTable']
results = collection.find()
print("results:", results)
# Create a list to store the individual image file objects and JSON data
image_file_objects = []
json_data_list = []

# Fetch BSON document containing JSON data
json_collection = db['jsonTable']
bson_document = json_collection.find_one({})

# Convert BSON to JSON
json_data = json_util.loads(json_util.dumps(bson_document))

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

for result in results:
    try:
        file_type = result['type']
        if file_type == 'image':
            data = result['data']
            image_data = bytes(data)
            img = Image.open(BytesIO(image_data))
            img = img.resize((400, 300))  # Resize the image to medium size
            image_file_objects.append(img)
            print("Image appended:", image_file_objects)

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

    except (KeyError, TypeError):
        print("exception")
        continue

print(f"Total images found: {len(image_file_objects)}")

# Calculate the number of pages
num_images_per_page = 10
num_pages = math.ceil(len(image_file_objects) / num_images_per_page)

# Create a Tkinter window and canvas
root = tk.Tk()
root.geometry("1200x600")

# Function to switch to the next page
def next_page():
    current_page = int(page_number.get())
    if current_page < num_pages:
        current_page += 1
        page_number.set(str(current_page))
        update_page()

# Function to switch to the previous page
def previous_page():
    current_page = int(page_number.get())
    if current_page > 1:
        current_page -= 1
        page_number.set(str(current_page))
        update_page()

# Create a frame for the left side (images and JSON data)
frame = tk.Frame(root)
frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a canvas for the images
canvas = tk.Canvas(frame, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar for the canvas
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add the scrollbar to the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame to hold the image labels and JSON text widgets
inner_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

# Create page navigation buttons
page_nav_frame = tk.Frame(root)
page_nav_frame.pack(side=tk.BOTTOM, pady=10)

previous_button = tk.Button(page_nav_frame, text="Previous", command=previous_page)
previous_button.pack(side=tk.LEFT, padx=10)

page_number = tk.StringVar()
page_number.set("1")

page_label = tk.Label(page_nav_frame, textvariable=page_number)
page_label.pack(side=tk.LEFT)

next_button = tk.Button(page_nav_frame, text="Next", command=next_page)
next_button.pack(side=tk.LEFT, padx=10)

# Update the displayed images based on the current page
def update_page():
    current_page = int(page_number.get())
    start_index = (current_page - 1) * num_images_per_page
    end_index = current_page * num_images_per_page

    # Clear the canvas
    for widget in inner_frame.winfo_children():
        widget.destroy()

    # Display images and JSON text for the current page
    for i, (image_file_object, json_data) in enumerate(zip(image_file_objects[start_index:end_index], json_data_list[start_index:end_index])):
        try:
            # Create an ImageTk object for the image
            photo = ImageTk.PhotoImage(image_file_object)

            # Create a label for the image
            label = tk.Label(inner_frame, image=photo)
            label.image = photo  # To prevent image garbage collection
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)

            # Determine the size of the image
            img_width, img_height = image_file_object.size

            # Create a Text widget for the JSON data with a border
            json_text = tk.Text(inner_frame, wrap=tk.WORD, height=int(img_height / 16), width=int(img_width / 3),
                                bd=1, relief=tk.SOLID)
            json_text.insert(tk.END, json_data)
            json_text.config(state=tk.DISABLED)  # Make the text widget read-only
            json_text.grid(row=i, column=1, padx=10, pady=10, sticky=tk.W)
        except Exception as e:
            print(f"Error displaying image: {e}")
            continue

    # Configure the canvas to adjust to the content size
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Update the page with initial data
update_page()

# Run the Tkinter event loop
root.mainloop()
