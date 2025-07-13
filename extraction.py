import cv2

# Extract frames at 1 FPS
def extract_frames(video_path: str, fps: int = 1):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    native_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(int(native_fps // fps), 1)

    frames, count = [], 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append(frame)
        count += 1

    cap.release()
    return frames