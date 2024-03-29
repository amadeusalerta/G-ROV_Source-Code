import cv2
from ultralytics import YOLO

class getModel:

    def __init__(self, pt_file_name, with_cuda = True):

        self.model = YOLO(pt_file_name)

        try:
            self.model.to("cuda" if with_cuda else "cpu")
        except:
            self.model.to("cpu")

    def getLocations(self, frame, names = None, imgsz = 640):

        results = self.model(frame, imgsz = imgsz)
        
        y_shape, x_shape = frame.shape[:2]

        self.objects = []

        for i in results[0]:

            self.obj = []

            for x1, y1, x2, y2, t, n in i.boxes.data:

                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                t = round(float(t), 2)

                self.obj = [x1, y1, x2, y2, t]

            for x in range(len(i.boxes[0])):
                
                n = i.boxes[0].cls[x]
                n = int(n)
                n = self.model.names[n]
                
                self.obj.append(n)

            self.objects.append(self.obj)

        if names is None:
            return self.objects

        else:

            names = [str(i) for i in names]

            self.locations = []

            for i in self.objects:
                if i[5] in names:
                    self.locations.append(i)

            return self.locations

    """def getLocations(self, frame):

        results = self.model(frame)
        
        y_shape, x_shape = frame.shape[:2]

        self.locations = []
        
        for values in results[0].boxes:
            
            x1 = int(values.boxes[0][0])
            y1 = int(values.boxes[0][1])
            x2 = int(values.boxes[0][2])
            y2 = int(values.boxes[0][3])

            t = round(float(values.boxes[0][4]), 2)

            self.locations.append([x1, y1, x2, y2, t])

        return self.locations"""

if __name__ == "__main__":

    cam = cv2.VideoCapture(0)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    model = getModel("yolov8s.pt", with_cuda = False)

    while True:

        ret, frame = cam.read()

        height, width = frame.shape[:2]

        frame = cv2.resize(frame, (640, 480))

        locations = model.getLocations(frame, None, 640)

        #print(locations)

        for (x1, y1, x2, y2, t, n) in locations:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"{n} {t}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 255), 2)

        cv2.imshow("CAM", frame)

        if cv2.waitKey(1) == ord("q"):
            break
    
    cam.release()

    cv2.destroyAllWindows()
