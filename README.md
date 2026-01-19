# **🎮** [GestureMouse](https://youtu.be/n14O1pGMJQQ) - Cursor Control 

Transform your webcam into a natural input device. Control your mouse cursor, click, scroll, and zoom using intuitive hand gestures. No touch required.

## Overview

GestureMouse is an open-source Windows application that replaces traditional mouse input with real-time hand gesture recognition. Using advanced computer vision and machine learning, your hand becomes your mouse. Point to move, pinch to click, and use multi-hand gestures for advanced interactions.

**Current Status**: Under active research and development.

---

## Hand Gesture Controls

### Single Hand Gestures

| Gesture | Action | How to Perform |
|---------|--------|----------------|
| **Index Finger Point** | Move cursor | Keep index finger extended upward, other fingers folded. Move hand smoothly across camera. |
| **Thumb + Index Pinch** | Left Click | Bring thumb and index fingertips together. Quick release = click, hold + move = drag. |
| **Thumb + Middle Pinch** | Right Click | Bring thumb and middle fingertips together. Release quickly for right-click menu. |
| **Index + Middle Pinch + Move** | Scroll | Pinch index and middle fingers, move hand up to scroll up, down to scroll down. |
| **Fist (All Fingers Closed)** | Pause Control | Make a tight fist. Cursor freezes until hand opens. |

### Dual Hand Gestures

| Gesture | Action | How to Perform |
|---------|--------|----------------|
| **Both Hands - Index Fingers Spread Apart** | Zoom Out | Extend index fingers on both hands, move hands away from each other. |
| **Both Hands - Index Fingers Bring Together** | Zoom In | Extend index fingers on both hands, bring them closer together. |

---

## Detailed Gesture Guide

### Cursor Movement - Index Finger Point

**How it works:**
- Extend only your **index finger** pointing upward
- All other fingers should be relaxed or folded
- Move your hand naturally in front of camera
- Your cursor tracks your index fingertip in real-time

**Tips for best results:**
- Keep hand within camera frame
- Maintain steady movements to avoid jitter
- Good lighting helps accuracy
- Camera should be at chest height, 2-3 feet away

### Left Click - Thumb + Index Pinch

**Single Click:**
1. Bring your thumb and index finger tips together (pinch)
2. Touch and immediately release (< 0.5 seconds)
3. Perfect for clicking buttons, links, and UI elements

**Drag Operation:**
1. Bring thumb and index together (pinch)
2. Hold the pinch (> 0.5 seconds) - drag begins
3. Move your hand while maintaining the pinch
4. Release pinch to drop the object

### Right Click - Thumb + Middle Pinch

**How to perform:**
1. Bring your thumb and middle finger tips together
2. Release quickly (< 0.5 seconds)
3. Context menu appears at cursor position

### Scroll - Index + Middle Pinch + Move

**How to perform:**
1. Bring index and middle finger tips together (pinch)
2. Move hand **upward** to scroll up
3. Move hand **downward** to scroll down
4. Release pinch to stop scrolling

### Pause Control - Fist Gesture

**Fist Gesture:**
1. Make a tight fist with all fingers folded
2. Cursor immediately stops responding
3. Open hand to resume control

### Zoom - Dual Hand Index Pinch & Spread

**Zoom Out:**
1. Extend index fingers on both hands
2. Move hands away from each other

**Zoom In:**
1. Extend index fingers on both hands
2. Bring hands together

---

## System Requirements

- **OS**: Windows 10 or later
- **Camera**: Any standard webcam
- **RAM**: Minimum 2GB
- **Processor**: Dual-core processor (2.4 GHz+)
- **Lighting**: Well-lit environment

---

## How to Use - For Normal Users

### Step 1: Download & Run

1. **Download** `GestureMouse.exe` from GitHub Releases
2. **Double-click** the file
3. **Click** "Run anyway" if Windows security prompt appears
4. **Allow** camera access when prompted

### Step 2: Use Application

- Position your webcam 2-3 feet away at chest height
- Extend your index finger to move cursor
- Use pinch gestures to click, scroll, zoom
- Make a fist to pause control

### Step 3: Close Application

**From System Tray:**
- Look for green circle icon (bottom-right corner)
- Right-click > **Exit**

**From Task Manager:**
- Press `Ctrl + Shift + Esc`
- Find "GestureMouse"
- Right-click > **End task**

**From Command Line:**
- Press `Windows Key + R`
- Type: `taskkill /IM GestureMouse.exe /F`
- Press Enter

---

## How to Setup - For Contributors

### Step 1: Clone Repository

```bash
git clone https://github.com/abhishekprajapatt/gesturemouse.git
cd gesturemouse
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Application

```bash
python main.py
```

### Step 5: Make Changes & Test

1. Edit files (main.py, etc.)
2. Run `python main.py` to test
3. Verify gesture controls work

### Step 6: Build EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name GestureMouse main.py
```

EXE will be in `dist/GestureMouse.exe`

---

## How to Contribute

### Step 1: Fork Repository

1. Go to GitHub repository
2. Click **Fork** button
3. Clone your fork:

```bash
git clone https://github.com/YOUR-USERNAME/gesturemouse.git
cd gesturemouse
```

### Step 2: Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Step 3: Make Changes

Edit files and test with `python main.py`

### Step 4: Commit & Push

```bash
git add .
git commit -m "Feature: Description of changes"
git push origin feature/your-feature-name
```

### Step 5: Create Pull Request

1. Go to GitHub repository
2. Click **Pull Request** button
3. Select your branch
4. Add description of changes
5. Submit PR

### Contribution Areas

- Gesture recognition improvements
- Performance optimization
- Bug fixes
- Documentation improvements
- Testing and feedback

---

## Project Structure

```
gesturemouse/
├── main.py                 # Main application
├── requirements.txt        # Dependencies
├── README.md              # This file
├── LICENSE                # GPL-3.0 License
├── build_exe.bat          # Build script
└── GestureMouse.spec      # PyInstaller config
```

---

## Common Commands

| Task | Command |
|------|---------|
| Run application | `python main.py` |
| Install dependencies | `pip install -r requirements.txt` |
| Build EXE | `pyinstaller --onefile --windowed --name GestureMouse main.py` |
| Activate virtual env | `venv\Scripts\activate` |
| Deactivate virtual env | `deactivate` |

---

## Troubleshooting

### Camera Not Detected

- Check Device Manager for camera
- Close other camera apps (Zoom, Teams)
- Go to Settings > Privacy & Security > Camera
- Enable camera access

### Cursor Jittering

- Improve lighting
- Keep hand steady
- Position 2-3 feet from camera

### Gestures Not Responding

- Ensure hand is visible in camera
- Keep fingers separated
- Make deliberate pinch motions

### Application Won't Close

**System Tray:** Right-click green icon > Exit

**Task Manager:** Ctrl + Shift + Esc > Find GestureMouse > End task

**Command:** `taskkill /IM GestureMouse.exe /F`

---

## Current Development Status

### ✅ Implemented

- [x] Real-time hand detection
- [x] Cursor movement with smooth tracking
- [x] Left click and drag
- [x] Right click gesture
- [x] Scroll (up/down)
- [x] Dual-hand zoom
- [x] Pause control (fist)
- [x] System tray integration

### 🔄 In Development

- [ ] Gesture sensitivity customization
- [ ] Settings interface
- [ ] Gesture recording

### 📋 Planned

- [ ] Cross-platform support (macOS, Linux)
- [ ] Voice command integration
- [ ] Macro recording

---

## Dependencies

- Python 3.7+
- opencv-python
- mediapipe
- pyautogui
- pystray
- pillow
- screeninfo

---

---

## Built With

- **[MediaPipe](https://mediapipe.dev/)** - Hand detection
- **[OpenCV](https://opencv.org/)** - Computer vision
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** - Mouse control
- **[PySTray](https://github.com/moses-palmer/pystray)** - System tray
- **[Pillow](https://python-pillow.org/)** - Image processing
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** - GUI

---

**Made with 💚 for natural human-computer interaction**

**Disclaimer**: GestureMouse is an ongoing research project. Use at your own risk in non-critical applications.
