import math
import cv2
from ultralytics import YOLOv10
from ultralytics.utils.plotting import Annotator, colors
import supervision as sv

# Load the model
model = YOLOv10("yolov10x.pt")
cap = cv2.VideoCapture("NascarTest.mp4")

# Get video properties
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Output video writer
out = cv2.VideoWriter("visioneye-distance-calculation.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))

# Define center point and pixel per meter ratio
#center_point = (w // 2, h // 2)  # Center of the frame
center_point = (w // 2, h)
pixel_per_meter = 100

# Colors for text and bounding box
txt_color, txt_background, bbox_clr = ((0, 0, 0), (255, 255, 255), (255, 0, 255))

while True:
    ret, im0 = cap.read()
    if not ret:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    annotator = Annotator(im0, line_width=2)
    results = model.track(im0, persist=True)
    boxes = results[0].boxes.xyxy.cpu()

    if results[0].boxes.id is not None:
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for box, track_id in zip(boxes, track_ids):
            annotator.box_label(box, label=str(track_id), color=bbox_clr)
            annotator.visioneye(box, center_point)

            # Calculate the centroid of the bounding box
            x1, y1 = int((box[0] + box[2]) // 2), int((box[1] + box[3]) // 2)

            # Calculate the distance from the centroid to the center point
            distance = (math.sqrt((x1 - center_point[0]) ** 2 + (y1 - center_point[1]) ** 2)) / pixel_per_meter

            # Display the distance on the frame
            text_size, _ = cv2.getTextSize(f"Distance: {distance:.2f} m", cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
            cv2.rectangle(im0, (x1, y1 - text_size[1] - 10), (x1 + text_size[0] + 10, y1), txt_background, -1)
            cv2.putText(im0, f"Distance: {distance:.2f} m", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.2, txt_color, 3)

    out.write(im0)
    cv2.imshow("visioneye-distance-calculation", im0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

out.release()
cap.release()
cv2.destroyAllWindows()
