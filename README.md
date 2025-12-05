# 🖐️ HandMouse AI — AI-Powered Hand Tracking Mouse Controller

HandMouse AI is a computer-vision project that lets you control your computer **entirely with hand gestures**, using a standard webcam.  
Inspired by AR/VR (XR) interaction systems like Meta Quest, this project uses:

- **MediaPipe Hands** → precise detection of 21 hand landmarks  
- **OpenCV** → real-time video processing  
- **PyAutoGUI** → system-level mouse control  
- **Automatic Vertical Calibration** → adapts instantly to any webcam and user  

No setup, no manual calibration — just run it and move your hand.

---

## 🚀 Features

### ✔ Full Mouse Control with Hand Gestures
- **Move cursor** → raise your index finger  
- **Left click** → pinch (thumb + index finger)  
- **Right click** → pinch (thumb + middle finger)  
- **Real-time tracking** with smooth or fast-response modes

### ✔ Automatic Vertical Calibration (PRO feature)
The system continually learns:

- your **highest** index-finger position  
- your **lowest** index-finger position  

and maps that range to **100% of the screen height**, enabling:

- reaching the taskbar and bottom icons  
- consistent behavior on any camera  
- adaptation to users of different heights and hand positions  
- instant adjustment when the camera moves or lighting changes  

### ✔ Extremely Smooth or Ultra-Responsive
Choose your preferred control style:

- `alpha = 1.0` → zero lag, XR-style, ultra-responsive  
- `alpha = 0.9` → smooth but still fast  

### ✔ Works with Any Webcam
No depth sensors or special hardware required.

---

## 📁 Project Structure

```

hand-mouse-controller/
│── src/
│   ├── main.py
│   ├── hand_tracker.py
│   ├── gesture_detector.py
│   ├── mouse_controller.py
│   ├── config.py
│   └── utils/
│       ├── smoothing.py
│       └── **init**.py
│
├── requirements.txt
├── README.md
└── .gitignore

````

---

## 🛠 Installation

### 1️⃣ Create virtual environment

```bash
python -m venv .venv
````

### 2️⃣ Activate the environment

**Windows**

```bash
.\.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Running the App

```bash
python src/main.py
```

Then:

* Raise only your **index finger** → move cursor
* Thumb + index → **Left Click**
* Thumb + middle finger → **Right Click**
* Move hand up/down → auto-calibration adapts to your range
* Press **ESC** or **Q** to exit

A message at the bottom of the window reminds you that calibration is automatic.

---

## 💡 How Automatic Vertical Calibration Works

The system continuously observes:

* the **minimum Y** position of your index finger
* the **maximum Y** position

As soon as it sees new extremes, it expands the range and maps that dynamic interval to:

```
index_finger_highest  →  top of the screen
index_finger_lowest   →  bottom of the screen
```

This ensures:

* full access to screen corners
* effortless access to bottom icons/taskbar
* correct behavior even if the webcam doesn’t see your whole arm
* seamless user adaptation

No manual steps required.

---

## 📦 Technologies Used

* **Python 3.8+**
* **OpenCV**
* **MediaPipe Hands**
* **PyAutoGUI**
* **NumPy**

---

## 🎯 Project Goal

To explore natural, hands-free interaction systems by combining computer vision and human-computer interaction (HCI), enabling new ways to control computers without physical input devices.

Great for:

* XR research
* HCI projects
* AI-driven interaction interfaces
* Real-time CV applications

---

## 👤 Author

Developed by **Jhonnatan Del Castillo**

Artificial Intelligence & Systems Engineering

Passionate about XR, computer vision, and next-gen human-computer interfaces.

---

## ⭐ Support the Project

If you like this:

* Star ⭐ the repo
* Share it
* Suggest new gestures (scroll, drag-and-drop, zoom, window controls, etc.)

Just Tell Me
---

