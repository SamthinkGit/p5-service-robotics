import GUI
import HAL
import pyapriltags
import yaml
from pathlib import Path
from typing import Any
import cv2

detector = pyapriltags.Detector(searchpath=["apriltags"], families="tag36h11")


def get_detections():
    image = HAL.getImage()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = detector.detect(gray)
    return results


def plot_detections(detections: Any):
    image = HAL.getImage()
    for r in detections:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(image, ptA, ptB, (0, 255, 0), 2)
        cv2.line(image, ptB, ptC, (0, 255, 0), 2)
        cv2.line(image, ptC, ptD, (0, 255, 0), 2)
        cv2.line(image, ptD, ptA, (0, 255, 0), 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        cv2.putText(
            image,
            tagFamily,
            (ptA[0], ptA[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
    GUI.showImage(image)


conf = yaml.safe_load(
    Path("/resources/exercises/marker_visual_loc/apriltags_poses.yaml").read_text()
)
tags = conf["tags"]

print("\n"*30)
print("="*30 + " Starting " + "="*30)
print(tags)
detections = get_detections()
for d in detections:
    print(d)
    print(f"{detections['tag_id']=}")
    print(f"{detections.homography=}")

while True:
    pass

