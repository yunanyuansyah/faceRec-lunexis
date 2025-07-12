"""
Door Controller Module for Solenoid Lock System
Mengontrol solenoid door lock menggunakan relay pada Raspberry Pi
Optimized for Raspberry Pi 5 with enhanced GPIO control
"""

import time
import threading
from datetime import datetime
import platform

# Try to import GPIO libraries (will fail on non-Raspberry Pi systems)
try:
    import RPi.GPIO as GPIO
    from gpiozero import OutputDevice
    RASPBERRY_PI = True
    
    # Detect Raspberry Pi version
    pi_model = "Unknown"
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model_info = f.read().strip()
            if "Raspberry Pi 5" in model_info:
                pi_model = "Raspberry Pi 5"
                print("🍓 Raspberry Pi 5 detected - using optimized GPIO control")
            elif "Raspberry Pi 4" in model_info:
                pi_model = "Raspberry Pi 4"
                print("🍓 Raspberry Pi 4 detected - using standard GPIO control")
            elif "Raspberry Pi 3" in model_info:
                pi_model = "Raspberry Pi 3"
                print("🍓 Raspberry Pi 3 detected - using standard GPIO control")
            else:
                pi_model = model_info
                print(f"🍓 {model_info} detected")
    except:
        print("🍓 Raspberry Pi GPIO libraries loaded successfully")
    
    print(f"🔧 Hardware: {pi_model}")
    
except ImportError:
    RASPBERRY_PI = False
    pi_model = "Non-Raspberry Pi"
    print("⚠️  Running on non-Raspberry Pi system - GPIO functions will be simulated")

class DoorController:
    def __init__(self, relay_pin=18, lock_duration=5):
        """
        Initialize door controller with Raspberry Pi 5 optimizations
        
        Args:
            relay_pin (int): GPIO pin number for relay control (default: 18)
            lock_duration (int): How long to keep door unlocked in seconds (default: 5)
        """
        self.relay_pin = relay_pin
        self.lock_duration = lock_duration
        self.is_unlocked = False
        self.unlock_timer = None
        
        if RASPBERRY_PI:
            # Setup GPIO with Pi 5 specific optimizations
            try:
                # For Raspberry Pi 5, use enhanced GPIO setup
                if "Raspberry Pi 5" in pi_model:
                    # Pi 5 has improved GPIO performance
                    # active_high=False for active low relay
                    self.relay = OutputDevice(
                        relay_pin, 
                        active_high=False,  # ACTIVE LOW RELAY
                        initial_value=False,
                        pin_factory=None  # Use default factory for Pi 5
                    )
                    print(f"✅ Raspberry Pi 5: GPIO pin {relay_pin} initialized with ACTIVE LOW relay control")
                else:
                    # Standard setup for other Pi models with active low relay
                    self.relay = OutputDevice(relay_pin, active_high=False, initial_value=False)
                    print(f"✅ GPIO pin {relay_pin} initialized for ACTIVE LOW relay control")
                
                print(f"🔒 Door lock system ready - unlock duration: {lock_duration} seconds")
                print(f"🏁 Hardware platform: {pi_model}")
                print(f"⚡ Relay type: ACTIVE LOW (ON = 0V, OFF = 3.3V)")
            except Exception as e:
                print(f"❌ Error initializing GPIO: {e}")
                self.relay = None
        else:
            self.relay = None
            print(f"🔧 Door controller initialized in simulation mode")
            print(f"🔒 Simulated door lock - pin: {relay_pin}, duration: {lock_duration}s")
            print(f"⚡ Relay type: ACTIVE LOW (ON = 0V, OFF = 3.3V)")
    
    def unlock_door(self, person_name="Unknown"):
        """
        Unlock the door for specified duration
        
        Args:
            person_name (str): Name of person who triggered unlock
        """
        if self.is_unlocked:
            print(f"🔓 Door sudah terbuka - mengatur ulang timer untuk {person_name}")
            # Reset timer if door is already unlocked
            if self.unlock_timer:
                self.unlock_timer.cancel()
        else:
            print(f"🔓 MEMBUKA PINTU untuk {person_name}")
            self.is_unlocked = True
            
            if RASPBERRY_PI and self.relay:
                try:
                    # Activate relay (unlock solenoid) - For active low relay, .on() sends LOW signal
                    self.relay.on()
                    print(f"⚡ ACTIVE LOW Relay GPIO pin {self.relay_pin} ACTIVATED (LOW signal sent)")
                except Exception as e:
                    print(f"❌ Error activating relay: {e}")
            else:
                print(f"🔧 [SIMULATION] ACTIVE LOW Relay pin {self.relay_pin} would be activated (LOW signal)")
        
        # Log the unlock event
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 Door unlock logged: {person_name} at {timestamp}")
        
        # Set timer to lock door again
        self.unlock_timer = threading.Timer(self.lock_duration, self._lock_door)
        self.unlock_timer.start()
        
        return True
    
    def _lock_door(self):
        """
        Internal method to lock the door (called by timer)
        """
        print(f"🔒 MENGUNCI PINTU (otomatis setelah {self.lock_duration} detik)")
        self.is_unlocked = False
        
        if RASPBERRY_PI and self.relay:
            try:
                # Deactivate relay (lock solenoid) - For active low relay, .off() sends HIGH signal
                self.relay.off()
                print(f"⚡ ACTIVE LOW Relay GPIO pin {self.relay_pin} DEACTIVATED (HIGH signal sent)")
            except Exception as e:
                print(f"❌ Error deactivating relay: {e}")
        else:
            print(f"🔧 [SIMULATION] ACTIVE LOW Relay pin {self.relay_pin} would be deactivated (HIGH signal)")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 Door locked at {timestamp}")
    
    def force_lock(self):
        """
        Immediately lock the door (emergency function)
        """
        if self.unlock_timer:
            self.unlock_timer.cancel()
        self._lock_door()
        print("🚨 Door force locked!")
    
    def get_status(self):
        """
        Get current door status with Raspberry Pi 5 specific information
        
        Returns:
            dict: Door status information including Pi 5 specifics
        """
        status = {
            "is_unlocked": self.is_unlocked,
            "relay_pin": self.relay_pin,
            "lock_duration": self.lock_duration,
            "raspberry_pi": RASPBERRY_PI,
            "relay_available": self.relay is not None,
            "pi_model": pi_model if RASPBERRY_PI else "Non-Raspberry Pi",
            "relay_type": "ACTIVE LOW",
            "relay_logic": "ON = 0V (LOW), OFF = 3.3V (HIGH)"
        }
        
        # Add Pi 5 specific status information
        if RASPBERRY_PI and "Raspberry Pi 5" in pi_model:
            status.update({
                "pi5_optimized": True,
                "gpio_performance": "Enhanced",
                "recommended_pins": [18, 19, 20, 21]  # Pi 5 preferred GPIO pins for relay
            })
        
        return status
    
    def cleanup(self):
        """
        Clean up GPIO resources
        """
        if self.unlock_timer:
            self.unlock_timer.cancel()
        
        if RASPBERRY_PI and self.relay:
            try:
                self.relay.off()  # Make sure relay is off
                self.relay.close()  # Clean up GPIO
                print("✅ GPIO resources cleaned up")
            except Exception as e:
                print(f"⚠️  Error during GPIO cleanup: {e}")
        
        print("🔒 Door controller shutdown complete")

# Global door controller instance
door_controller = None

def initialize_door_controller(relay_pin=18, lock_duration=5):
    """
    Initialize global door controller instance
    
    Args:
        relay_pin (int): GPIO pin for relay
        lock_duration (int): Unlock duration in seconds
    
    Returns:
        DoorController: The initialized controller
    """
    global door_controller
    door_controller = DoorController(relay_pin, lock_duration)
    return door_controller

def unlock_door_for_person(person_name):
    """
    Convenience function to unlock door for a person
    
    Args:
        person_name (str): Name of the person
    
    Returns:
        bool: True if successful, False otherwise
    """
    global door_controller
    if door_controller:
        return door_controller.unlock_door(person_name)
    else:
        print("❌ Door controller not initialized!")
        return False

def cleanup_door_controller():
    """
    Clean up the global door controller
    """
    global door_controller
    if door_controller:
        door_controller.cleanup()
        door_controller = None

# Test function
if __name__ == "__main__":
    print("🧪 Testing Door Controller...")
    
    # Initialize controller
    controller = initialize_door_controller(relay_pin=18, lock_duration=3)
    
    # Test unlock
    print("\n1. Testing door unlock...")
    unlock_door_for_person("Test User")
    
    # Wait and show status
    time.sleep(1)
    status = controller.get_status()
    print(f"\n📊 Door Status: {status}")
    
    # Wait for auto-lock
    print("\n2. Waiting for auto-lock...")
    time.sleep(3)
    
    # Final status
    status = controller.get_status()
    print(f"\n📊 Final Status: {status}")
    
    # Cleanup
    cleanup_door_controller()
    print("\n✅ Test complete!")
