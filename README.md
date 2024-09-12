---

## **Ball Hit Detection Project**

This project is part of a Python Machine Learning Jam and is designed to detect when a tennis ball hits a designated area on a wall and translate the hit to a virtual white screen. Both the physical frame and virtual screen maintain a 16:9 aspect ratio. 

### **Project Overview**

The system uses a webcam to detect ball hits within a taped-off frame on a wall. When a hit is detected, it translates the point of impact onto a corresponding virtual white screen on the computer. This project demonstrates how machine learning techniques can be applied to real-world problems like motion detection and mapping in a creative, scalable way.

---

### **Core Features**

- **Frame Setup**: A 16:9 aspect ratio frame is created on a wall using colored tape, and the system can scale between a minimum of 32 inches diagonal to 200 inches diagonal.
  
- **Ball Hit Detection**: Detects tennis ball hits inside the frame using image processing and displays the corresponding location on a virtual white screen.
  
- **Impact Visualization**: The hit is visualized by a black circle displayed on the white screen at the exact point of impact.

- **Calibration**: The system calibrates to any frame size within the supported range, ensuring accurate mapping between the physical and virtual frames.

- **Noise Reduction**: Strategies are implemented to reduce false positives, ensuring only actual hits are detected.

---

### **System Requirements**

- Python 3.x
- OpenCV (for image processing)
- Numpy (for array manipulation)
- Webcam
- Tennis balls
- Colored tape for creating the frame on the wall

---

### **Installation Instructions**

#### **Step 1: Clone the Repository**
```bash
git clone https://github.com/CH-Anonymous/ball-hit-detection-project.git
```

#### **Step 2: Install Dependencies**
Before running the project, ensure you have the necessary Python libraries installed.

```bash
pip install numpy opencv-python
```

#### **Step 3: Run the Project**
Run the `ball_hit_detection.py` script:(If this not working try It manually to run)

```bash
python src/ball_hit_detection.py
```

---

### **Setup Instructions**

#### **1. Create the Frame on the Wall**
- Use colored tape to create a **16:9 aspect ratio** frame on the wall.
- The frame can be any size within the range of **32 inches diagonal** to **200 inches diagonal**.
- Example size: 32 inches diagonal, which is approximately **28 inches width** x **15.75 inches height**.

#### **2. Position the Webcam**
- Set up your webcam facing the framed area.
- Ensure the camera captures the entire frame clearly.

#### **3. Run the Python Script**
- The script will use the webcam to detect ball hits within the frame.
- Hits are visualized as black circles on a virtual white screen displayed on your computer.

---

### **How It Works**

1. **Frame and Camera Calibration**: The system first calibrates the frame and maps the frame's dimensions onto the virtual white screen.
2. **Ball Hit Detection**: When a tennis ball is thrown at the wall, the system uses image processing (via OpenCV) to detect any changes in the frame, especially identifying movements (the ball).
3. **Impact Point Mapping**: Once a hit is detected, the point of impact is calculated and then visualized as a black dot on the virtual white screen, maintaining proportionality with the physical frame.
4. **Noise Reduction**: The system uses various filters and thresholding techniques to minimize false positives caused by other movements or lighting changes.

---

### **Project Structure**

```bash
ball-hit-detection-project/
│
├── README.md                
├── src/
│   └── ball_hit_detection.py 
└── assets/
    └── demo_video.mp4  


```

---

### **Future Enhancements**

- Improve hit detection accuracy under varying lighting conditions.
- Allow for dynamic resizing of the frame during operation.
- Implement sound feedback when a hit is detected.

---

### **Contributing**

---

### **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

This `README.md` provides a complete description of your project, making it easy for anyone to understand how to set up, use, and contribute to the project. Make sure to include any demo video or images you have to make the submission even more compelling.
