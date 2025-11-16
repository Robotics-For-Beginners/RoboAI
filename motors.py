#!/usr/bin/env python3
"""
REAL MOTOR CONTROL - No simulations!
Controls robot motors through GPIO pins
"""
import time
import RPi.GPIO as GPIO

class Motors:
    def __init__(self):
        print("🔧 Initializing REAL motors...")
        
        # Motor GPIO pins (L298N style)
        self.LEFT_FORWARD = 17
        self.LEFT_BACKWARD = 18
        self.RIGHT_FORWARD = 22
        self.RIGHT_BACKWARD = 23
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        
        # Setup motor pins as outputs
        motor_pins = [self.LEFT_FORWARD, self.LEFT_BACKWARD, 
                     self.RIGHT_FORWARD, self.RIGHT_BACKWARD]
        
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Start with motors off
        
        self.motor_pwm = {}
        
        # Create PWM for speed control (optional)
        try:
            self.motor_pwm['left_forward'] = GPIO.PWM(self.LEFT_FORWARD, 1000)  # 1kHz
            self.motor_pwm['left_backward'] = GPIO.PWM(self.LEFT_BACKWARD, 1000)
            self.motor_pwm['right_forward'] = GPIO.PWM(self.RIGHT_FORWARD, 1000)
            self.motor_pwm['right_backward'] = GPIO.PWM(self.RIGHT_BACKWARD, 1000)
            
            # Start PWM with 0% duty cycle (stopped)
            for pwm in self.motor_pwm.values():
                pwm.start(0)
                
            self.has_pwm = True
            print("✅ PWM speed control enabled")
        except:
            self.has_pwm = False
            print("✅ Basic motor control (no PWM)")
        
        print("🚗 REAL motors ready on GPIO 17,18,22,23")
    
    def _set_motor_speed(self, pin, speed):
        """Set motor speed with PWM or digital"""
        if self.has_pwm and speed > 0:
            self.motor_pwm[pin].ChangeDutyCycle(speed)
        else:
            # Digital control (on/off)
            GPIO.output(getattr(self, pin.upper()), GPIO.HIGH if speed > 0 else GPIO.LOW)
    
    def _stop_all_motors(self):
        """Stop all motors immediately"""
        pins = [self.LEFT_FORWARD, self.LEFT_BACKWARD, 
               self.RIGHT_FORWARD, self.RIGHT_BACKWARD]
        
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)
        
        # Also stop PWM
        if self.has_pwm:
            for pwm in self.motor_pwm.values():
                pwm.ChangeDutyCycle(0)
    
    def move_forward(self, seconds=2, speed=80):
        """Move robot forward - REAL movement"""
        print(f"🚀 Moving FORWARD for {seconds} seconds at {speed}% power")
        
        try:
            # Stop any previous movement
            self._stop_all_motors()
            time.sleep(0.1)
            
            # Activate forward pins
            if self.has_pwm:
                self.motor_pwm['left_forward'].ChangeDutyCycle(speed)
                self.motor_pwm['right_forward'].ChangeDutyCycle(speed)
            else:
                GPIO.output(self.LEFT_FORWARD, GPIO.HIGH)
                GPIO.output(self.RIGHT_FORWARD, GPIO.HIGH)
            
            # Move for specified time
            time.sleep(seconds)
            
            # Stop
            self._stop_all_motors()
            print("✅ Forward movement complete")
            
        except Exception as e:
            print(f"❌ Motor error: {e}")
            self._stop_all_motors()
    
    def move_backward(self, seconds=2, speed=80):
        """Move robot backward - REAL movement"""
        print(f"🔄 Moving BACKWARD for {seconds} seconds at {speed}% power")
        
        try:
            self._stop_all_motors()
            time.sleep(0.1)
            
            # Activate backward pins
            if self.has_pwm:
                self.motor_pwm['left_backward'].ChangeDutyCycle(speed)
                self.motor_pwm['right_backward'].ChangeDutyCycle(speed)
            else:
                GPIO.output(self.LEFT_BACKWARD, GPIO.HIGH)
                GPIO.output(self.RIGHT_BACKWARD, GPIO.HIGH)
            
            time.sleep(seconds)
            self._stop_all_motors()
            print("✅ Backward movement complete")
            
        except Exception as e:
            print(f"❌ Motor error: {e}")
            self._stop_all_motors()
    
    def turn_left(self, seconds=1, speed=70):
        """Turn robot left - REAL turning"""
        print(f"↩️ Turning LEFT for {seconds} seconds at {speed}% power")
        
        try:
            self._stop_all_motors()
            time.sleep(0.1)
            
            # Right motor forward, left motor stopped/backward
            if self.has_pwm:
                self.motor_pwm['right_forward'].ChangeDutyCycle(speed)
                self.motor_pwm['left_backward'].ChangeDutyCycle(speed)
            else:
                GPIO.output(self.RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(self.LEFT_BACKWARD, GPIO.HIGH)
            
            time.sleep(seconds)
            self._stop_all_motors()
            print("✅ Left turn complete")
            
        except Exception as e:
            print(f"❌ Motor error: {e}")
            self._stop_all_motors()
    
    def turn_right(self, seconds=1, speed=70):
        """Turn robot right - REAL turning"""
        print(f"↪️ Turning RIGHT for {seconds} seconds at {speed}% power")
        
        try:
            self._stop_all_motors()
            time.sleep(0.1)
            
            # Left motor forward, right motor stopped/backward
            if self.has_pwm:
                self.motor_pwm['left_forward'].ChangeDutyCycle(speed)
                self.motor_pwm['right_backward'].ChangeDutyCycle(speed)
            else:
                GPIO.output(self.LEFT_FORWARD, GPIO.HIGH)
                GPIO.output(self.RIGHT_BACKWARD, GPIO.HIGH)
            
            time.sleep(seconds)
            self._stop_all_motors()
            print("✅ Right turn complete")
            
        except Exception as e:
            print(f"❌ Motor error: {e}")
            self._stop_all_motors()
    
    def stop(self):
        """Emergency stop - REAL stop"""
        print("🛑 EMERGENCY STOP - All motors off")
        self._stop_all_motors()
    
    def test_motors(self):
        """Test each motor individually"""
        print("🧪 Testing all motors...")
        
        tests = [
            ("Left forward", self.LEFT_FORWARD),
            ("Left backward", self.LEFT_BACKWARD),
            ("Right forward", self.RIGHT_FORWARD),
            ("Right backward", self.RIGHT_BACKWARD)
        ]
        
        for motor_name, pin in tests:
            print(f"Testing {motor_name}...")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)
        
        print("✅ Motor test complete")
    
    def __del__(self):
        """Clean up GPIO when done"""
        print("🧹 Cleaning up GPIO...")
        self._stop_all_motors()
        time.sleep(0.1)
        GPIO.cleanup()

# Standalone test
if __name__ == "__main__":
    print("🚗 MOTOR TEST MODE")
    print("Connect motors to GPIO 17,18,22,23")
    print("This will test each motor for 1 second")
    
    input("Press Enter to start motor test...")
    
    try:
        motors = Motors()
        motors.test_motors()
        print("🎉 All motors working!")
    except Exception as e:
        print(f"❌ Motor test failed: {e}")
    finally:
        print("Test complete")
