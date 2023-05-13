import cv2
import uuid

import time
import pickle

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

all_coordinates = []
objects = {}
in_count = 0
out_count = 0

def counting(x, y, r1=(0, 150), r2=(150, 300)):
    global in_count, out_count
    r = 0
    if y > r1[0] and y <= r1[1]: #1, 150
        r = 1
    elif y > r2[0] and y < r2[1]: #151, 299
        r = 2
    c = [x, y, str(uuid.uuid4()), r]
    all_coordinates.append(c)
    req_dist = 40
    index_to_pop = []
    u_id = ""
    if len(all_coordinates) > 1:
        for index in range(len(all_coordinates)-1):
            c1 = all_coordinates[index]
            for i in all_coordinates[index+1:]:
                abs_dist = int(((c1[0]-i[0])**2 + (c1[1]-i[1])**2)**0.5)
#                 print(abs_dist)
                if abs_dist < req_dist:
                    i[2] = c1[2]
                    u_id = c1[2]
                    index_to_pop.append(index)
                    if c1[2] in objects:
                        #print("ID:",c1[2],end=" ")
                        #print("Previous:",objects[c1[2]][-1][-1],end=" ")
                        #print("Current:",c1[-1])
                        if objects[c1[2]][-1][-1] == 1 and c1[-1] == 2:
                            in_count += 1
                            #print("inc", end="")
                        if objects[c1[2]][-1][-1] == 2 and c1[-1] == 1:
                            out_count += 1
                            #print("dec", end="")
                        #print()
                        objects[c1[2]].append(c1)
                    else:
                        objects[c1[2]] = [c1]
        for ele in index_to_pop[::-1]:
            all_coordinates.pop(ele)
    coordinates_len = len(all_coordinates)
    if coordinates_len > 20:
        for _ in range(coordinates_len - 20):
            all_coordinates.pop(0)

    #print("all coordinates", all_coordinates)
    #print("objects", objects)
    return u_id

def cal_centroid(detections):
    coordinates = []
    for i in detections:
        i = i.bounding_box
        ymin = i.origin_y
        ymax = i.origin_y + i.height
        xmin = i.origin_x
        xmax = i.origin_x + i.width
        x_center = int((xmax + xmin) // 2)
        y_center = int((ymax + ymin) // 2)
        coordinates.append([int(ymin), int(xmin), int(ymax), int(xmax), x_center, y_center])

    return coordinates

def store_data(data):
    with open('/home/kamaleshpathy/Downloads/final_test/value.pkl', 'wb') as f:
        pickle.dump(data, f)

def main():
    # Frame rate
    #fps = 0

    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    f_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    base_options = core.BaseOptions(file_name='/home/kamaleshpathy/Downloads/final_test/detect_new_1.tflite', use_coral=False, num_threads=4)

    detection_options = processor.DetectionOptions(max_results=10, score_threshold=0.5)

    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)

    detector = vision.ObjectDetector.create_from_options(options)

    flag = False

    start_time = time.time()

    while cap.isOpened():
        success, image = cap.read()

        # Frame rate
        #tStart = time.time()

        image = cv2.flip(image, 1)

        if flag:
            flag = False
            continue

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = vision.TensorImage.create_from_array(rgb_image)
        detection_result = detector.detect(input_tensor)
        #if len(detection_result.detections) != 0:
            #print(detection_result.detections[0].bounding_box)
            #print(detection_result.detections[0].categories[0].score)
        centroid_coordinates = cal_centroid(detection_result.detections)
        #cv2.line(image, (0, int(f_height/2)), (640, int(f_height/2)), (255, 255, 255), 2)

        for position in centroid_coordinates:
            cv2.circle(image, (position[4], position[5]), 2, (255, 255, 128), 2)
            the_id = counting(position[4], position[5], (0, int(f_height/2)),(int(f_height/2), f_height))
            cv2.putText(image, the_id, (position[4]+10, position[5]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 128), 1)
            out_text = f"In: {in_count} | Out: {out_count}"
            print(out_text)

        # image = utils.visualize(image, detection_result)

        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('object_detector', image)
        end_time = time.time()
        if end_time - start_time > 0.5:
            start_time = end_time
            store_data(f"{in_count},{out_count}")

        flag = True
        
        #Frame rate
        #tEnd = time.time()
        #loopTime = tEnd - tStart
        #fps = .9*fps + .1*(1/loopTime)

        #print(fps)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            continue
#    main()
