Object Detection Studio

Object Detection Studio is a desktop application built with Python, Tkinter, and YOLO to perform real-time or static image object detection. It allows users to upload an image, run YOLO-based detection, visualize bounding boxes with labels, and perform additional image processing operations such as Laplacian edge transformation.

✨ Features

User–friendly GUI using Tkinter

Load images locally for detection

YOLO model–based object recognition

Randomized box colors for visual clarity

Detection confidence filtering

Save detection results to file

Clear / reset interface

Laplace transform image processing

Supports standard image formats (JPG, PNG, etc.)

🧠 Model Used

The application uses the lightweight YOLOv8n model:

yolov8n.pt


This model is included with the project and does not require additional downloading.

📁 Project Structure
math_project/
│
├── kid.py                  # Main Python executable
├── detection_result.jpg    # Example output image
├── yolov8n.pt              # YOLOv8 model
└── tempCodeRunnerFile.py   # temp execution artifact

🔧 Installation & Requirements
1. Install Python

Make sure you have Python 3.8+ installed.

2. Install dependencies
pip install opencv-python Pillow numpy ultralytics


Tkinter is typically included in standard Python builds.

▶️ Running the Application
python kid.py


The GUI will launch and display the main interface.

🖼️ How to Use

Click "Select Image" to upload an input image

Press "Detect" to run object detection

Results are displayed with bounding boxes and labels

Optionally apply:

Laplace Transform

Optionally clear to reset

Final output can be saved as detection_result.jpg

📸 Example Output

Detections appear with labeled objects such as:

person

dog

cat

car

etc.

Bounding boxes are drawn in dynamically assigned colors.

🧮 Laplace Transform Feature

The app includes a grayscale Laplacian operator for edge detection:

cv2.Laplacian(image, cv2.CV_64F)


This can be applied to any selected image and viewed in the GUI.

🏫 Academic Context

This project was developed as part of a 3rd-year academic requirement, demonstrating practical knowledge in:

Computer Vision

GUI development

Machine learning model integration

Python programming

Digital image processing
