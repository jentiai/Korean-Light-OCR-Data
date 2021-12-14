import os

def remove_labels_no_image(image_files, label_path):
    image_list = list(image_files.keys())

    for (path, dir, files) in os.walk(label_path):
        files = list(files)
        for file in files:
            if file.replace('.txt', '.jpg') not in image_list:
                os.remove(os.path.join(path, file))

# def remove_no_gt(label_path):
#     for (path, dir, files) in os.walk(label_path):
#         files = list(files)
        
#         for file in files:
#             file_size = os.path.getsize(os.path.join(path, file))
#             if file_size == 0:
#                 os.remove(os.path.join(path, file))