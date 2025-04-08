import os
import sys
import json
import cv2 

###########

def load_and_parse_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)  # Load JSON data

    # Parse the data
    parsed_data = []
    for entry in data:
        x, y, idx = entry
        parsed_data.append({'x': x, 'y': y, 'idx': idx})

    return parsed_data

###############


crowdUIT_images_folders = r"D:\Datasets\CrowdUIT\CrowdUIT\Crowd-UIT\Image"
crowdUIT_jsons_folders = r"D:\Datasets\CrowdUIT\CrowdUIT\Crowd-UIT\Json"

img_folders = []
json_folders = []

for img_folder in os.listdir(crowdUIT_images_folders):
    img_folders.append(os.path.join(crowdUIT_images_folders, img_folder))

for json_folder in os.listdir(crowdUIT_jsons_folders):
    json_folders.append(os.path.join(crowdUIT_jsons_folders, json_folder))

img_folders = sorted(img_folders)
json_folders = sorted(json_folders)



for img_folder, json_folder in zip(img_folders, json_folders):
    print(img_folder, json_folder)
    images_list = []
    jsons_list = []

    sequencenumber = img_folder.split("\\")[-1]

    for imagefile, jsonfile in zip((os.listdir(img_folder)), (os.listdir(json_folder)) ):
        framenumber = imagefile.split(".")[0]
        print(os.path.join(img_folder, imagefile), os.path.join(json_folder, jsonfile) ) #debug
        imagefile_full_path = os.path.join(img_folder, imagefile)
        jsonfile_full_path = os.path.join(json_folder, jsonfile)

        image = cv2.imread(imagefile_full_path)
        img_height, img_width, channels = image.shape
        json_data = load_and_parse_json(jsonfile_full_path)

        for item in json_data:
            x = item['x']
            y = item['y']
            idx = item['idx']
            cv2.circle(image, center=(x,y), radius=3, color=(0,255,0), thickness=-1)
            cv2.putText(image, f"{idx}", (x-3, y-3), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0,255,255), thickness=1)
            cv2.putText(image, f"Seq:{sequencenumber} Frame:{framenumber}", (10, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255,255,255), thickness=2)

        cv2.imshow("image", image)
        destination_folder_to_write = os.path.join(img_folder, f"viz") 
        destination_to_write = os.path.join(destination_folder_to_write, f"{framenumber}.jpg") 
        if not os.path.exists(destination_folder_to_write):
            os.makedirs(destination_folder_to_write)
        cv2.imwrite(destination_to_write, image)

cv2.destroyAllWindows