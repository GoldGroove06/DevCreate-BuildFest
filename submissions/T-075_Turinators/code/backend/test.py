import cv2
import os
import shutil
from ultralytics import YOLO
import numpy as np

def process_video(input_path, model_name, frame: int = 6):
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    OUTPUT_FOLDER = "outputs"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    model_path = model_name
    video_path = os.path.join(UPLOAD_FOLDER, input_path)
    output_video_path = os.path.join(OUTPUT_FOLDER, input_path)
    temp_dir = os.path.join(OUTPUT_FOLDER, "temp_frames")

    fps_extract = frame

    model = YOLO(model_path)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / fps_extract)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(temp_dir, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1
        frame_count += 1

    cap.release()
    print(f" Extracted {saved_count} frames into {temp_dir}")

    processed_dir = os.path.join(temp_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    for filename in sorted(os.listdir(temp_dir)):
        if not filename.endswith(".jpg"):
            continue
        frame_path = os.path.join(temp_dir, filename)
        results = model(frame_path)
      

        # Get frame dimensions
        frame_yolo = results[0].plot()
        height, width = frame_yolo.shape[:2]
        mid_x = width // 2

        # Check if masks exist
        if results[0].masks is not None:
            pothole_data = []
            
            # Collect polygon data for each detection
            for i, poly in enumerate(results[0].masks.xy):
                polygon = np.array(poly, dtype=np.int32)  # (N,2) points
                area = cv2.contourArea(polygon)
                
                # Calculate centroid of polygon
                M = cv2.moments(polygon)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = polygon[0]
                
                # Determine side (left or right of center)
                side = "left" if cx < mid_x else "right"
                
                pothole_data.append({
                    'index': i,
                    'polygon': polygon,
                    'area': area,
                    'centroid': (cx, cy),
                    'side': side
                })
                
                print(f"Polygon {i+1} → Area: {area:.2f} pixels² | Side: {side}")
            
            # Count potholes in vertical 75% region (top to 75% of height)
            vertical_75_threshold = int(height * 0.75)
            potholes_in_75 = [p for p in pothole_data if p['centroid'][1] <= vertical_75_threshold]
            
            # CASE 3: More than 3 potholes in front 75% vertical region
            if len(potholes_in_75) >= 3:
                cv2.putText(frame_yolo, "SLOW SPEED", 
                            (width//2 - 150, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                cv2.putText(frame_yolo, " MULTIPLE POTHOLES AHEAD", 
                            (width//2 - 250, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            
            # CASE 1 & 2: Directional guidance
            elif len(pothole_data) > 0:
                # Separate by side
                left_potholes = [p for p in pothole_data if p['side'] == 'left']
                right_potholes = [p for p in pothole_data if p['side'] == 'right']
                
                # CASE 1: Only one pothole OR potholes on one side only
                if len(left_potholes) == 0 and len(right_potholes) > 0:
                    # Potholes on right, show arrow pointing left
                    draw_arrow(frame_yolo, "LEFT", width, height)
                    
                elif len(right_potholes) == 0 and len(left_potholes) > 0:
                    # Potholes on left, show arrow pointing right
                    draw_arrow(frame_yolo, "RIGHT", width, height)
                
                # CASE 2: Potholes on both sides
                elif len(left_potholes) > 0 and len(right_potholes) > 0:
                    # Calculate total area on each side
                    left_total_area = sum(p['area'] for p in left_potholes)
                    right_total_area = sum(p['area'] for p in right_potholes)
                    
                    # Point away from bigger pothole area
                    if left_total_area > right_total_area:
                        draw_arrow(frame_yolo, "RIGHT", width, height)
                        print(f"Left area ({left_total_area:.2f}) > Right area ({right_total_area:.2f}) → Go RIGHT")
                    else:
                        draw_arrow(frame_yolo, "LEFT", width, height)
                        print(f"Right area ({right_total_area:.2f}) > Left area ({left_total_area:.2f}) → Go LEFT")


            def draw_arrow(frame, direction, width, height):
                """Draw a red directional arrow on the frame"""
                arrow_color = (0, 0, 255)  # Red in BGR
                thickness = 8
                
                if direction == "LEFT":
                    # Draw left arrow in left portion of frame
                    arrow_start = (int(width * 0.3), height // 2)
                    arrow_end = (int(width * 0.1), height // 2)
                    
                    # Main arrow line
                    cv2.arrowedLine(frame, arrow_start, arrow_end, 
                                arrow_color, thickness, tipLength=0.5)
                    
                    # Text
                    cv2.putText(frame, "← GO LEFT", 
                            (int(width * 0.05), height // 2 - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, arrow_color, 3)
                
                elif direction == "RIGHT":
                    # Draw right arrow in right portion of frame
                    arrow_start = (int(width * 0.7), height // 2)
                    arrow_end = (int(width * 0.9), height // 2)
                    
                    # Main arrow line
                    cv2.arrowedLine(frame, arrow_start, arrow_end, 
                                arrow_color, thickness, tipLength=0.5)
                    
                    # Text
                    cv2.putText(frame, "GO RIGHT →", 
                            (int(width * 0.65), height // 2 - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, arrow_color, 3)

        else:
            print("No polygons detected")
    
        cv2.imwrite(os.path.join(processed_dir, filename), frame_yolo)

    print(f" Processed frames saved into {processed_dir}")

    first_frame = cv2.imread(os.path.join(processed_dir, sorted(os.listdir(processed_dir))[0]))
    height, width, _ = first_frame.shape

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps_extract, (width, height))

    for filename in sorted(os.listdir(processed_dir)):
        frame_path = os.path.join(processed_dir, filename)
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    print(f" Output video saved as {output_video_path}")
    return input_path
