# Function to reindex annotations in text files based on a standard label map.

import yaml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def reindex_annotations(annotation_folder, data_yaml_file, standard_label_map):
    """
    Reindex annotations in text files based on a standard label map.

    This function reads annotation files from a specified folder, updates the class indices
    according to a provided standard label map, and writes the updated annotations back to the files.
    It also logs the changes made to the class indices.

    Args:
        annotation_folder (str): Path to the folder containing annotation text files.
        data_yaml_file (str): Path to the YAML file containing current label names.
        standard_label_map (dict): A dictionary mapping current label names to new indices.

    Returns:
        None
    """
    # Load current YAML to get the current labels
    with open(data_yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # List of current label names
    current_labels = data["names"]
    logging.info("Current Label Names: %s", current_labels)

    # Extract the current mapping (label names and current index)
    current_label_map = {name: idx for idx, name in enumerate(current_labels)}
    logging.info("Current Label Mapping: %s", current_label_map)

    # Iterate through all the files in the annotation folder
    for filename in os.listdir(annotation_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(annotation_folder, filename)

            # Read all lines from the file
            with open(file_path, "r") as file:
                lines = file.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue

                # Get the old index and label name
                old_index = int(parts[0])
                old_label_name = current_labels[old_index]

                # Handle the case where the label name is not in the standard map
                if old_label_name not in standard_label_map:
                    logging.warning(
                        "File: %s - Class '%s' not found in the standard label map",
                        filename,
                        old_label_name,
                    )
                    continue

                # Get the new index from the standard label map
                new_index = standard_label_map.get(old_label_name, old_index)
                logging.info(
                    "File: %s - Class '%s' - Old Index: %d, New Index: %d",
                    filename,
                    old_label_name,
                    old_index,
                    new_index,
                )

                if old_index != new_index:
                    new_line = f"{new_index} {' '.join(parts[1:])}"
                    new_lines.append(new_line)

            # Write the updated lines back to the file
            with open(file_path, "w") as file:
                for new_line in new_lines:
                    file.write(f"{new_line}\n")

    # Update the YAML file with the new label names
    updated_yaml_file = data.copy()
    updated_yaml_file["names"] = list(standard_label_map.keys())
    updated_yaml_file["nc"] = len(standard_label_map)
    with open(data_yaml_file, "w") as f:
        yaml.dump(updated_yaml_file, f)
    logging.info("Updated YAML file: %s", data_yaml_file)
    logging.info("COMPLETED")


############################################## Driver Code ##############################################


# Define standard label map
standard_label_map = {
    "angryface": 0,
    "auto": 1,
    "bicycle": 2,
    "bus": 3,
    "car": 4,
    "happyface": 5,
    "motorcycle": 6,
    "neutralface": 7,
    "numberplate": 8,
    "person": 9,
    "pole": 10,
    "road": 11,
    "road_cross": 12,
    "sadface": 13,
    "sidewalk": 14,
    "truck": 15,
    "van": 16,
}

# Path of the files
annotation_folder = "Test/Labels/train"


data_yaml_file = "Test/dataset.yaml"

reindex_annotations(annotation_folder, data_yaml_file, standard_label_map)
