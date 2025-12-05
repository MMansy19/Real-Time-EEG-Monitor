# Installation Guide - NeuroViz Pro

## Quick Start

### Windows

#### Prerequisites
1. **Python 3.8+**
   ```powershell
   # Check Python version
   python --version
   
   # If not installed, download from:
   # https://www.python.org/downloads/
   ```

2. **Git** (optional, for cloning)
   ```powershell
   # Download from: https://git-scm.com/download/win
   git --version
   ```

#### Installation Steps

1. **Clone or Download Repository**
   ```powershell
   # Method 1: Clone with Git
   git clone https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor.git
   cd NeuroViz-Pro-EEG-Monitor
   
   # Method 2: Download ZIP
   # Extract to desired location
   cd path\to\NeuroViz-Pro-EEG-Monitor
   ```

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```powershell
   # Simulation mode
   python codeV1.py
   
   # Arduino mode
   python codeV2.py
   ```

---

### macOS

#### Prerequisites
1. **Python 3.8+**
   ```bash
   # Check Python version
   python3 --version
   
   # Install via Homebrew (if needed)
   brew install python3
   ```

2. **Command Line Tools**
   ```bash
   xcode-select --install
   ```

#### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor.git
   cd NeuroViz-Pro-EEG-Monitor
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Arduino Setup** (if using hardware)
   ```bash
   # Find Arduino port
   ls /dev/tty.*
   # Look for /dev/tty.usbmodem* or /dev/tty.usbserial*
   
   # Update codeV2.py with correct port
   SERIAL_PORT = "/dev/tty.usbmodem14101"  # Example
   ```

5. **Run Application**
   ```bash
   python3 codeV1.py  # Simulation
   python3 codeV2.py  # Arduino
   ```

---

### Linux (Ubuntu/Debian)

#### Prerequisites
1. **Python 3.8+**
   ```bash
   # Check version
   python3 --version
   
   # Install if needed
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Development Tools**
   ```bash
   sudo apt install build-essential git
   ```

3. **Qt Dependencies**
   ```bash
   sudo apt install python3-pyqt5 libqt5gui5
   ```

#### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor.git
   cd NeuroViz-Pro-EEG-Monitor
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Arduino Permissions** (if using hardware)
   ```bash
   # Add user to dialout group
   sudo usermod -a -G dialout $USER
   
   # Logout and login for changes to take effect
   # Or temporarily:
   sudo chmod 666 /dev/ttyUSB0  # Or your Arduino port
   
   # Find Arduino port
   ls /dev/ttyUSB* /dev/ttyACM*
   ```

5. **Run Application**
   ```bash
   python3 codeV1.py  # Simulation
   python3 codeV2.py  # Arduino
   ```

---

## Troubleshooting Installation

### Issue: `pip install` fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement PyQt5
```

**Solution:**
```bash
# Update pip
python -m pip install --upgrade pip

# Try with --user flag
pip install --user -r requirements.txt

# Or install packages individually
pip install numpy scipy PyQt5 pyqtgraph pyserial
```

---

### Issue: PyQt5 import error on Linux

**Error:**
```
ImportError: libQt5Core.so.5: cannot open shared object file
```

**Solution:**
```bash
# Install Qt5 libraries
sudo apt install python3-pyqt5 libqt5widgets5 libqt5gui5 libqt5core5a

# Or use conda (alternative)
conda install pyqt
```

---

### Issue: Serial port access denied

**Error:**
```
serial.serialutil.SerialException: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

**Solution:**
```bash
# Method 1: Add user to dialout group (permanent)
sudo usermod -a -G dialout $USER
# Then logout/login

# Method 2: Temporary permission
sudo chmod 666 /dev/ttyUSB0

# Method 3: Use sudo (not recommended)
sudo python3 codeV2.py
```

---

### Issue: Virtual environment activation fails

**Windows PowerShell:**
```powershell
# If execution policy blocks activation
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
venv\Scripts\activate
```

**Linux/macOS:**
```bash
# Ensure script is executable
chmod +x venv/bin/activate
source venv/bin/activate
```

---

## Arduino Setup

### Hardware Requirements
- Arduino Uno, Nano, or Mega
- EEG sensor module (e.g., AD8232, OpenBCI)
- USB cable

### Arduino Code Example

Upload this sketch to your Arduino:

```cpp
// Simple EEG simulator for NeuroViz Pro
// Outputs values to serial at 1000 Hz

unsigned long lastTime = 0;
const int interval = 1;  // 1ms = 1000 Hz

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastTime >= interval) {
    lastTime = currentTime;
    
    // Read from analog pin A0 (EEG sensor)
    int value = analogRead(A0);
    
    // Or simulate a signal
    // float t = currentTime / 1000.0;
    // int value = 512 + 50*sin(2*PI*10*t) + random(-10, 10);
    
    Serial.println(value);
  }
}
```

### Connecting EEG Sensor

```
Arduino          AD8232 Module
─────────────────────────────
3.3V     ───────> VCC
GND      ───────> GND
A0       ───────> OUTPUT
```

---

## Verification

### Test Installation

```python
# test_installation.py
import sys
print(f"Python version: {sys.version}")

try:
    import numpy as np
    print(f"✓ NumPy {np.__version__}")
except:
    print("✗ NumPy not found")

try:
    import scipy
    print(f"✓ SciPy {scipy.__version__}")
except:
    print("✗ SciPy not found")

try:
    from PyQt5 import QtWidgets
    print(f"✓ PyQt5 installed")
except:
    print("✗ PyQt5 not found")

try:
    import pyqtgraph
    print(f"✓ PyQtGraph {pyqtgraph.__version__}")
except:
    print("✗ PyQtGraph not found")

try:
    import serial
    print(f"✓ PySerial {serial.__version__}")
except:
    print("✗ PySerial not found")

print("\nIf all packages show ✓, installation is complete!")
```

Run:
```bash
python test_installation.py
```

---

## Next Steps

After successful installation:

1. **Read the README**: `README.md` for overview
2. **Configure settings**: Edit `USE_ARDUINO` in code
3. **Run simulation**: `python codeV1.py`
4. **Connect Arduino** (optional): Update `SERIAL_PORT`
5. **Explore documentation**: `DOCUMENTATION.md` and `WORKFLOW.md`

---

## Getting Help

- **GitHub Issues**: [Report problems](https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor/issues)
- **Discussions**: [Ask questions](https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor/discussions)
- **Documentation**: See `docs/` folder

---

*Last updated: December 5, 2025*
