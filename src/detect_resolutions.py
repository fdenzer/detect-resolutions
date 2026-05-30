import cv2
import platform

# Import the camera detection logic from our existing script
from detect_cameras import list_ports

def test_resolutions(port_index, backend_preference=None):
    """
    Attempts to set various standard resolutions on the given camera port
    to discover which ones are natively supported by the hardware and driver.
    """
    # A comprehensive list of standard 4:3, 16:9, and other common resolutions
    candidate_resolutions = [
        (160, 120),
        (320, 240),
        (426, 240),
        (640, 360),
        (640, 480),
        (800, 600),
        (960, 540),
        (1024, 768),
        (1280, 720),    # HD 720p
        (1280, 960),
        (1440, 1080),
        (1600, 1200),
        (1920, 1080),   # Full HD 1080p
        (2048, 1536),
        (2560, 1440),   # QHD 2K
        (3200, 2400),
        (3840, 2160),   # 4K UHD
    ]
    
    supported_resolutions = set()
    
    # Open the camera
    current_os = platform.system()
    if current_os == "Windows" and backend_preference:
        cap = cv2.VideoCapture(port_index, backend_preference)
    else:
        cap = cv2.VideoCapture(port_index)
        
    if not cap.isOpened():
        print(f"Could not open camera {port_index} to test resolutions.")
        return []
        
    print(f"\nTesting camera {port_index}...")
    
    # We will try to set each resolution and see what the driver snaps it to
    for w, h in candidate_resolutions:
        # Request width and height
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        
        # Read back what the camera driver actually set
        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Try reading a frame at this resolution to verify it works
        is_reading, _ = cap.read()
        
        if is_reading and actual_w > 0 and actual_h > 0:
            supported_resolutions.add((actual_w, actual_h))
            
    cap.release()
    
    # Sort resolutions by area (width * height)
    sorted_resolutions = sorted(list(supported_resolutions), key=lambda x: x[0] * x[1])
    return sorted_resolutions

def main():
    print("Detecting active cameras first...")
    # Dynamically find active ports using the imported detection script
    working_cameras = list_ports()
    
    if not working_cameras:
        print("No active cameras were detected. Exiting resolution discovery.")
        return
        
    active_ports = [cam["port"] for cam in working_cameras]
    
    current_os = platform.system()
    backend_preference = cv2.CAP_DSHOW if current_os == "Windows" else None
    
    print("\nBeginning comprehensive resolution discovery...")
    print("=" * 60)
    
    for port in active_ports:
        resolutions = test_resolutions(port, backend_preference)
        print(f"\n[+] Supported resolutions for Camera {port}:")
        if resolutions:
            for w, h in resolutions:
                aspect_ratio = f"{w/h:.2f}"
                # Human readable common labels
                label = ""
                if (w, h) == (1280, 720): label = " (HD 720p)"
                elif (w, h) == (1920, 1080): label = " (FHD 1080p)"
                elif (w, h) == (3840, 2160): label = " (4K UHD)"
                elif (w, h) == (640, 480): label = " (VGA 480p)"
                
                print(f"    - {w}x{h} [Aspect Ratio: {aspect_ratio}]{label}")
        else:
            print("    No resolutions could be successfully queried.")
            
    print("=" * 60)

if __name__ == "__main__":
    main()
