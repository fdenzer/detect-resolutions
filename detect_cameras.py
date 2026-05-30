import cv2
import platform

def list_ports():
    """
    Finds and lists all active camera indices/ports using OpenCV.
    Uses an OS-specific backend codeswitch to ensure maximum compatibility.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    
    # --- OS CODESWITCH FOR BACKEND ---
    current_os = platform.system()
    print(f"Running on: {current_os}")
    
    if current_os == "Windows":
        # DirectShow (CAP_DSHOW) unlocks high resolutions & avoids slow startup on Windows
        backend_preference = cv2.CAP_DSHOW
        print("Using DirectShow (CAP_DSHOW) backend for Windows compatibility.")
    else:
        # macOS (AVFoundation) and Linux (V4L2) work best with the default auto-selection
        backend_preference = cv2.CAP_ANY
        print("Using default OpenCV auto-backend selection.")
        
    print("Searching for connected cameras...")
    print("-" * 60)
    
    # Check the first 10 indices (usually sufficient for most workstations)
    while len(non_working_ports) < 6:
        # Try opening the camera with the selected backend configuration
        if current_os == "Windows":
            cap = cv2.VideoCapture(dev_port, backend_preference)
        else:
            cap = cv2.VideoCapture(dev_port)
        
        if not cap.isOpened():
            non_working_ports.append(dev_port)
        else:
            is_reading, img = cap.read()
            w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            backend = cap.getBackendName()
            
            if is_reading:
                print(f"[*] Camera index {dev_port} is working!")
                print(f"    - Default Resolution: {int(w)}x{int(h)}")
                print(f"    - API Backend: {backend}")
                working_ports.append({
                    "port": dev_port,
                    "width": w,
                    "height": h,
                    "backend": backend
                })
            else:
                print(f"[!] Camera index {dev_port} present but failed to read a frame.")
                
            cap.release()
            
        dev_port += 1
        
    print("-" * 60)
    if working_ports:
        print(f"Found {len(working_ports)} active camera(s): {[port['port'] for port in working_ports]}")
    else:
        print("No active cameras found.")
        
    return working_ports

if __name__ == "__main__":
    list_ports()
