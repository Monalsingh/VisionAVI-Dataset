# Import Essential Libraries
import cv2
import os


# Function to extract frames from a video (every 3 seconds)
def extract_frames(video_path, output_path, interval=3):
    """
    Extract frames from a video at a specified interval and save them as images.

    Parameters:
    video_path (str): Path to the input video file.
    output_path (str): Directory where the extracted frames will be saved.
    interval (int): Time interval (in seconds) between each frame to be extracted. Default is 3 seconds.

    Returns:
    None
    """
    # Read the video from specified path
    cap = cv2.VideoCapture(video_path)
    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)

    # Read the video frame by frame
    count = 0
    frame_count = 0
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Save the frame to the output path at the specified interval
            if count % frame_interval == 0:
                cv2.imwrite(os.path.join(output_path, f"frame{frame_count}.jpg"), frame)
                frame_count += 1
            count += 1
        else:
            break

    # Release the VideoCapture object
    cap.release()
    # Close all the frames
    cv2.destroyAllWindows()
    print("Frames extracted successfully!")


# Driver Code
video_paths = [
    "data/raw/IMG_4760.MOV",
    "data/raw/IMG_4762.MOV",
    "data/raw/IMG_4763.MOV",
    "data/raw/IMG_4765.MOV",
]

output_path = "data/raw_images/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

for video_path in video_paths:
    extract_frames(video_path, output_path)
