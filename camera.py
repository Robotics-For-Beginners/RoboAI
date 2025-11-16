#!/usr/bin/env python3
"""
REAL CAMERA VISION - No simulations!
Uses actual USB camera to see the real world
"""
import cv2
import time
import os

class Camera:
    def __init__(self):
        print("📷 Initializing REAL camera...")
        
        self.camera_index = 0  # /dev/video0
        self.cap = None
        self.connected = False
        
        # Try to connect to camera
        self._connect_camera()
    
    def _connect_camera(self):
        """Connect to actual USB camera"""
        try:
            print(f"🔌 Connecting to camera /dev/video{self.camera_index}...")
            self.cap = cv2.VideoCapture(self.camera_index)
            
            # Test if camera works
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.connected = True
                    print(f"✅ Camera connected! Resolution: {frame.shape[1]}x{frame.shape[0]}")
                else:
                    print("❌ Camera connected but can't read frames")
                    self.cap.release()
            else:
                print("❌ Cannot open camera")
                
        except Exception as e:
            print(f"❌ Camera error: {e}")
    
    def capture(self):
        """Capture REAL image from camera"""
        if not self.connected:
            return "Camera not available"
        
        try:
            # Capture frame
            ret, frame = self.cap.read()
            
            if not ret:
                return "Failed to capture image"
            
            # Save the image so we can analyze it
            timestamp = int(time.time())
            filename = f"camera_capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            
            # Analyze what we see
            analysis = self._analyze_frame(frame)
            
            print(f"📸 Captured image: {filename}")
            return analysis
            
        except Exception as e:
            return f"Camera error: {e}"
    
    def _analyze_frame(self, frame):
        """Analyze what the camera sees"""
        try:
            # Get basic image info
            height, width = frame.shape[:2]
            
            # Convert to HSV for color analysis
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Calculate brightness
            brightness = frame.mean()
            
            # Detect edges (simple object detection)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_count = cv2.countNonZero(edges)
            
            # Determine scene type
            if brightness < 50:
                scene = "dark room"
            elif brightness < 100:
                scene = "dimly lit area"
            elif brightness > 200:
                scene = "bright area"
            else:
                scene = "normally lit room"
            
            # Check if there are objects (edges)
            if edge_count > 10000:
                objects = "multiple objects"
            elif edge_count > 5000:
                objects = "some objects"
            else:
                objects = "few objects"
            
            return f"{scene} with {objects}, image size {width}x{height}"
            
        except Exception as e:
            return f"image analysis failed: {e}"
    
    def show_live_view(self, duration=5):
        """Show live camera feed - REAL preview"""
        if not self.connected:
            print("❌ Camera not available for live view")
            return
        
        print(f"👀 Showing live camera view for {duration} seconds...")
        print("Press 'q' to close early")
        
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration:
                ret, frame = self.cap.read()
                if ret:
                    # Display the frame
                    cv2.imshow('Robot Camera - Live View', frame)
                    
                    # Break if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("❌ Lost camera connection")
                    break
            
            cv2.destroyAllWindows()
            print("✅ Live view closed")
            
        except Exception as e:
            print(f"❌ Live view error: {e}")
            cv2.destroyAllWindows()
    
    def get_resolution(self):
        """Get actual camera resolution"""
        if not self.connected:
            return "Unknown"
        
        try:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return f"{width}x{height}"
        except:
            return "Unknown"
    
    def __del__(self):
        """Release camera when done"""
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()

# Standalone camera test
if __name__ == "__main__":
    print("📷 CAMERA TEST MODE")
    print("Make sure USB camera is connected")
    
    cam = Camera()
    
    if cam.connected:
        print(f"Camera resolution: {cam.get_resolution()}")
        
        # Test capture
        print("\n📸 Testing capture...")
        result = cam.capture()
        print(f"Camera sees: {result}")
        
        # Test live view
        print("\n👀 Testing live view (5 seconds)...")
        cam.show_live_view(5)
        
        print("🎉 Camera test complete!")
    else:
        print("❌ Camera test failed - check connections") 
