# Function to rename image and label files in a folder with a base name.

import os


def rename_files(image_folder, label_folder, base_name):
    """
    Rename files in the specified image and label folders with a given base name.

    This function renames all files in the `image_folder` and `label_folder` by appending
    a sequential number to the `base_name` provided. The renaming is done in-place.

    Parameters:
    image_folder (str): The path to the folder containing image files to be renamed.
    label_folder (str): The path to the folder containing label files to be renamed.
    base_name (str): The base name to use for renaming the files.

    Returns:
    None
    """

    # List all the files in the directory
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".jpg")])
    label_files = sorted([f for f in os.listdir(label_folder) if f.endswith(".txt")])

    # Check if the number of images and labels are the same
    if len(image_files) != len(label_files):
        print("Number of images and labels are not the same")
    else:
        print(
            "Number of images and labels are the same - Starting the Renaming Process"
        )

    # Renaming the images and labels simultaneously with the same name
    for i in range(len(image_files)):
        # Check if image and label have the same name
        if image_files[i].split(".")[0] == label_files[i].split(".")[0]:
            new_img_name = base_name + "_" + str(i) + ".jpg"
            new_label_name = base_name + "_" + str(i) + ".txt"
            os.rename(
                os.path.join(image_folder, image_files[i]),
                os.path.join(image_folder, new_img_name),
            )
            os.rename(
                os.path.join(label_folder, label_files[i]),
                os.path.join(label_folder, new_label_name),
            )
        else:
            print(f"{image_files[i]} and {label_files[i]} do not have the same name")

    print("COMPLETED RE-NAMING")


# Example usage
image_folder = "-------------------"
label_folder = "-------------------"
base_name = "KNCVB10065"  # MY ID
rename_files(image_folder, label_folder, base_name)
