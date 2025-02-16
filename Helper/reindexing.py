# Import Libraries
import yaml
import os
import logging

logging.basicConfig(level=logging.INFO)


def update_labels(annotation_folder, data_yaml_file, standard_label_map):
    """
    Update labels to match standard_label_map while preserving bounding box associations
    """
    # Load current YAML
    with open(data_yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # Create reverse mapping from current indices to label names
    current_idx_to_name = {idx: name for idx, name in enumerate(data["names"])}

    # Update data.yaml to match standard order
    data["names"] = [name for name in standard_label_map.keys()]
    data["nc"] = len(standard_label_map)

    # Write updated data.yaml
    with open(data_yaml_file, "w") as f:
        yaml.dump(data, f)
    logging.info("Updated data.yaml with standard label order")

    # Update annotation files
    for filename in os.listdir(annotation_folder):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(annotation_folder, filename)
        updated_lines = []

        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            # Get current label name using the old index
            old_idx = int(parts[0])
            if old_idx not in current_idx_to_name:
                logging.warning(f"Invalid label index {old_idx} in {filename}")
                continue

            label_name = current_idx_to_name[old_idx]
            if label_name not in standard_label_map:
                logging.warning(f"Skipping unknown label {label_name} in {filename}")
                continue

            # Get new index from standard map
            new_idx = standard_label_map[label_name]

            # Keep original bounding box coordinates
            new_line = f"{new_idx} {' '.join(parts[1:])}\n"
            updated_lines.append(new_line)

        # Write updated annotations
        with open(file_path, "w") as f:
            f.writelines(updated_lines)

    logging.info("Completed updating annotation files")


# Your existing paths and standard_label_map
annotation_folder = (
    "/Users/akb/Desktop/CV_GenAi/Project/visionaid/Data/anantha.k/train/labels"
)
data_yaml_file = (
    "/Users/akb/Desktop/CV_GenAi/Project/visionaid/Data/anantha.k/data.yaml"
)
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
    "sadface": 12,
    "sidewalk": 13,
    "truck": 14,
    "van": 15,
    "road_cross": 16,
}

# Run the update
update_labels(annotation_folder, data_yaml_file, standard_label_map)
