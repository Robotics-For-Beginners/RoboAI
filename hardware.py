#!/usr/bin/env python3
"""
Auto-detects what hardware is connected
"""
import subprocess
import os

class Hardware:
    def __init__(self):
        self.components = {}
        self.scan_hardware()
    
    def scan_hardware(self):
        """Scan for connected hardware"""
        print("🔍 Scanning your hardware...")
        
        # Check if Raspberry Pi
        if os.path.exists('/proc/device-tree/model'):
            with open('/proc/device-tree/model', 'r') as f:
                self.components['board'] = f.read().strip()
        else:
            self.components['board'] = "Computer"
        
        # Check for camera
        self.components['camera'] = self.check_camera()
        
        # Check for GPIO devices (assume common setup)
        self.components['motors'] = "GPIO 17,18,22,23 (assumed)"
        self.components['led'] = "GPIO 4 (assumed)"
        
        print("✅ Hardware scan complete!")
    
    def check_camera(self):
        """Check if camera is available"""
        try:
            # Try to access camera
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    return "Connected (/dev/video0)"
            return "Not found"
        except:
            return "Error checking"
    
    def summary(self):
        """Create simple hardware summary"""
        parts = []
        if 'board' in self.components:
            parts.append(f"Board: {self.components['board']}")
        if 'camera' in self.components:
            parts.append(f"Camera: {self.components['camera']}")
        if 'motors' in self.components:
            parts.append(f"Motors: {self.components['motors']}")
        if 'led' in self.components:
            parts.append(f"LED: {self.components['led']}")
        
        return ", ".join(parts) 
