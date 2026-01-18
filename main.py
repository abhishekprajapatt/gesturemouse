import cv2
import mediapipe as mp
import pyautogui
import pystray
import tkinter as tk
from PIL import Image, ImageDraw
import threading
import winreg
import os
import math
from screeninfo import get_monitors

class GestureMouse:
    def __init__(self):
        self.running = True
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = None
        self.cursor_x, self.cursor_y = 0, 0
        self.prev_x, self.prev_y = 0, 0
        self.smoothing_factor = 0.25
        self.pinch_start_time = {}
        self.pinch_threshold = 0.05
        self.dragging = False
        self.first_run = self.check_first_run()
        self.screen_width = get_monitors()[0].width
        self.screen_height = get_monitors()[0].height
        pyautogui.FAILSAFE = False
        
    def check_first_run(self):
        config_path = os.path.join(os.path.expanduser('~'), '.gesturemouse')
        if not os.path.exists(config_path):
            os.makedirs(config_path)
            return True
        return False
    
    def mark_first_run_done(self):
        config_path = os.path.join(os.path.expanduser('~'), '.gesturemouse', 'setup_done')
        with open(config_path, 'w') as f:
            f.write('done')
    
    def add_to_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
            exe_path = os.path.abspath(os.sys.executable if hasattr(os.sys, 'frozen') else __file__)
            if hasattr(os.sys, 'frozen'):
                exe_path = os.sys.executable
            winreg.SetValueEx(key, 'GestureMouse', 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        except:
            pass
    
    def show_overlay(self):
        overlay = tk.Tk()
        overlay.attributes('-fullscreen', True)
        overlay.attributes('-alpha', 0.85)
        overlay.configure(bg='#000000')
        
        canvas = tk.Canvas(overlay, bg='#000000', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        text = """GestureMouse Active

• Point with index finger → Move cursor
• Thumb + Index pinch → Left click / Hold for drag
• Thumb + Middle pinch → Right click
• Index + Middle pinch + move → Scroll
• Both hands index pinch & spread/close → Zoom in/out
• Fist or hand away → Pause

Running in background..."""
        
        canvas.create_text(
            self.screen_width // 2,
            self.screen_height // 2,
            text=text,
            font=('Arial', 32, 'bold'),
            fill='#00FF00',
            justify=tk.CENTER
        )
        
        def close_overlay():
            overlay.destroy()
        
        overlay.after(15000, close_overlay)
        overlay.mainloop()
    
    def init_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            root = tk.Tk()
            root.withdraw()
            from tkinter import messagebox
            messagebox.showerror('Camera Error', 'Could not access camera. GestureMouse will exit.')
            return False
        return True
    
    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
    
    def hand_size(self, landmarks):
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        return self.distance(wrist, middle_mcp)
    
    def is_fist(self, landmarks):
        wrist = landmarks[0]
        for i in [4, 8, 12, 16, 20]:
            if self.distance(wrist, landmarks[i]) > 0.15:
                return False
        return True
    
    def is_finger_extended(self, landmarks, tip_idx, pip_idx):
        return landmarks[tip_idx].y < landmarks[pip_idx].y
    
    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if not results.multi_hand_landmarks:
            return
        
        num_hands = len(results.multi_hand_landmarks)
        
        if num_hands == 1:
            landmarks = results.multi_hand_landmarks[0]
            if self.is_fist(landmarks.landmark):
                return
            
            index_extended = self.is_finger_extended(landmarks.landmark, 8, 6)
            if index_extended:
                index_pos = landmarks.landmark[8]
                self.cursor_x = int(index_pos.x * self.screen_width)
                self.cursor_y = int(index_pos.y * self.screen_height)
                
                smoothed_x = int(self.prev_x + (self.cursor_x - self.prev_x) * self.smoothing_factor)
                smoothed_y = int(self.prev_y + (self.cursor_y - self.prev_y) * self.smoothing_factor)
                
                self.prev_x, self.prev_y = smoothed_x, smoothed_y
                pyautogui.moveTo(smoothed_x, smoothed_y, duration=0)
            
            h_size = self.hand_size(landmarks.landmark)
            threshold = h_size * self.pinch_threshold
            
            thumb = landmarks.landmark[4]
            index = landmarks.landmark[8]
            middle = landmarks.landmark[12]
            
            thumb_index_dist = self.distance(thumb, index)
            thumb_middle_dist = self.distance(thumb, middle)
            index_middle_dist = self.distance(index, middle)
            
            if thumb_index_dist < threshold:
                if 'left' not in self.pinch_start_time:
                    self.pinch_start_time['left'] = cv2.getTickCount()
                    self.dragging = False
                else:
                    elapsed = (cv2.getTickCount() - self.pinch_start_time['left']) / cv2.getTickFrequency()
                    if elapsed > 0.5 and not self.dragging:
                        pyautogui.mouseDown()
                        self.dragging = True
            else:
                if 'left' in self.pinch_start_time:
                    elapsed = (cv2.getTickCount() - self.pinch_start_time['left']) / cv2.getTickFrequency()
                    if elapsed < 0.5 and not self.dragging:
                        pyautogui.click()
                    elif self.dragging:
                        pyautogui.mouseUp()
                        self.dragging = False
                    del self.pinch_start_time['left']
            
            if thumb_middle_dist < threshold:
                if 'right' not in self.pinch_start_time:
                    self.pinch_start_time['right'] = cv2.getTickCount()
            else:
                if 'right' in self.pinch_start_time:
                    elapsed = (cv2.getTickCount() - self.pinch_start_time['right']) / cv2.getTickFrequency()
                    if elapsed < 0.5:
                        pyautogui.click(button='right')
                    del self.pinch_start_time['right']
            
            if index_middle_dist < threshold:
                hand_center_y = (index.y + middle.y) / 2
                if hand_center_y < 0.3:
                    pyautogui.scroll(5)
                elif hand_center_y > 0.7:
                    pyautogui.scroll(-5)
        
        elif num_hands == 2:
            landmarks_1 = results.multi_hand_landmarks[0]
            landmarks_2 = results.multi_hand_landmarks[1]
            
            index_1 = landmarks_1.landmark[8]
            index_2 = landmarks_2.landmark[8]
            
            current_dist = self.distance(index_1, index_2)
            
            if hasattr(self, 'prev_hand_dist'):
                dist_change = current_dist - self.prev_hand_dist
                if dist_change > 0.05:
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(-3)
                    pyautogui.keyUp('ctrl')
                elif dist_change < -0.05:
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(3)
                    pyautogui.keyUp('ctrl')
            
            self.prev_hand_dist = current_dist
    
    def camera_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            self.process_frame(frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    def on_exit_tray(self, icon, item):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        icon.stop()
    
    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color='black')
        draw = ImageDraw.Draw(image)
        draw.ellipse([10, 10, 54, 54], fill='green', outline='white')
        
        menu = pystray.Menu(pystray.MenuItem('Exit', self.on_exit_tray))
        icon = pystray.Icon('GestureMouse', image, menu=menu)
        icon.run()
    
    def run(self):
        self.add_to_startup()
        
        if not self.init_camera():
            return
        
        if self.first_run:
            overlay_thread = threading.Thread(target=self.show_overlay, daemon=True)
            overlay_thread.start()
            self.mark_first_run_done()
        
        camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        camera_thread.start()
        
        self.create_tray_icon()

if __name__ == '__main__':
    app = GestureMouse()
    app.run()