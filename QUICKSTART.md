# Quick Start Guide - NeuroViz Pro

## 5-Minute Setup

### For Beginners

#### Step 1: Install Python
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

#### Step 2: Download Project
- **Option A**: Download ZIP from GitHub
  - Click green "Code" button → Download ZIP
  - Extract to your desired location
  
- **Option B**: Clone with Git
  ```bash
  git clone https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor.git
  ```

#### Step 3: Install Dependencies
Open terminal/command prompt in project folder:
```bash
pip install -r requirements.txt
```

#### Step 4: Run Application
```bash
# Start with simulation (no hardware needed)
python codeV1.py
```

🎉 **Done!** The application should launch with live EEG simulation.

---

## Understanding the Interface

### Main Window Layout

```
┌──────────────────────────────────────────────────────────────┐
│  ⚡ NEUROVIZ PRO    |    🟡 Simulation Mode    |  00:00:00   │ HEADER
├────────┬─────────────────────────────────────────────────────┤
│        │                                                     │
│ CONTROL│  ┌─────────────────────────────────────────────┐  │
│ PANEL  │  │         TIME DOMAIN PLOT                     │  │
│        │  │         (Rolling 2-second window)            │  │
│ Stats  │  └─────────────────────────────────────────────┘  │
│ ──────│                                                     │
│Samples:│  ┌──────────────────┐  ┌──────────────────────┐  │
│ 12,345 │  │  FFT SPECTRUM    │  │   SPECTROGRAM        │  │
│        │  │  (0-100 Hz)      │  │   (Time-Frequency)   │  │
│ Avg:   │  │                  │  │                      │  │
│  45 μV │  └──────────────────┘  └──────────────────────┘  │
│        │                                                     │
│ Buttons│  ┌─────────────────────────────────────────────┐  │
│ ───────│  │ δ:25%  θ:15%  α:40%  β:15%  γ:5%           │  │ BANDS
│● START │  └─────────────────────────────────────────────┘  │
│💾 SAVE │                                                     │
│🔄 CLEAR│                                                     │
└────────┴─────────────────────────────────────────────────────┘
```

### What You're Seeing

1. **Time Plot**: Live EEG signal (filtered, 1-50 Hz)
2. **FFT Spectrum**: Frequency components (peaks show dominant rhythms)
3. **Spectrogram**: Time-frequency evolution (colors = intensity)
4. **Band Indicators**: Percentage of each brain wave type
5. **Statistics**: Real-time metrics

---

## Using the Controls

### Recording Data

1. **Start Recording**
   - Click "● START RECORDING"
   - Button changes to "⏹ STOP RECORDING"
   - Data is captured in memory

2. **Stop Recording**
   - Click "⏹ STOP RECORDING"
   - "💾 SAVE DATA" button becomes active

3. **Save Data**
   - Click "💾 SAVE DATA"
   - Choose filename and location
   - Data saved as CSV file

### Example CSV Output
```csv
Sample,Value
1,512.34
2,515.67
3,510.23
...
```

### Other Controls

- **🔄 CLEAR**: Reset all displays and counters
- **✕ Close**: Exit application (automatically stops recording)

---

## Two Operating Modes

### Mode 1: Simulation (Default)
**When to use:** Testing, learning, no hardware available

**How to activate:**
```python
# In code file (codeV1.py)
USE_ARDUINO = False
```

**What it does:**
- Generates realistic brain wave signals
- Combines Delta, Theta, Alpha, Beta, Gamma waves
- Adds realistic noise
- Perfect for demonstrations

**Advantages:**
✓ No equipment needed  
✓ Instant start  
✓ Controlled signals  
✓ Educational use  

---

### Mode 2: Arduino Hardware
**When to use:** Real EEG measurements, research projects

**How to activate:**
```python
# In code file (codeV2.py)
USE_ARDUINO = True
SERIAL_PORT = "COM3"  # Change to your port
```

**Requirements:**
- Arduino board (Uno, Nano, Mega)
- EEG sensor (e.g., AD8232)
- USB cable

**Setup Steps:**
1. Connect EEG sensor to Arduino
2. Upload Arduino code (see INSTALLATION.md)
3. Connect Arduino to computer via USB
4. Find COM port (Device Manager on Windows)
5. Update `SERIAL_PORT` in code
6. Run `python codeV2.py`

**Advantages:**
✓ Real physiological data  
✓ Clinical applications  
✓ Research-grade  
✓ Subject monitoring  

**Automatic Fallback:**
If Arduino connection fails, system automatically switches to simulation mode.

---

## Interpreting the Display

### Brain Wave Bands

| Band | Frequency | When You See It | Color |
|------|-----------|----------------|-------|
| **Delta (δ)** | 0.5-4 Hz | Deep sleep, unconscious | Red |
| **Theta (θ)** | 4-8 Hz | Drowsy, meditative | Cyan |
| **Alpha (α)** | 8-13 Hz | Relaxed, eyes closed | Blue |
| **Beta (β)** | 13-30 Hz | Active thinking, alert | Yellow |
| **Gamma (γ)** | 30-50 Hz | High cognition, focus | Purple |

### Typical Patterns

**Relaxed State:**
- High Alpha (40-60%)
- Low Beta (10-20%)
- Minimal Delta/Theta

**Active Thinking:**
- High Beta (40-60%)
- Moderate Alpha (20-30%)
- Low Delta/Theta

**Drowsy/Sleepy:**
- High Theta (40-60%)
- Increasing Delta
- Decreasing Alpha/Beta

---

## Common Tasks

### Task 1: Record 1 Minute of Data

1. Launch application
2. Click "● START RECORDING"
3. Wait 60 seconds (watch timer)
4. Click "⏹ STOP RECORDING"
5. Click "💾 SAVE DATA"
6. Name file: `recording_1min.csv`
7. Click Save

**Result:** CSV file with ~60,000 samples (1000 Hz × 60 sec)

---

### Task 2: Export 5-Minute Session

Same as Task 1, but wait 5 minutes.

**Result:** ~300,000 samples in CSV

---

### Task 3: Analyze Alpha Waves

1. Have subject close eyes
2. Watch Alpha band indicator
3. Should increase to 50-80%
4. Have subject open eyes
5. Alpha should decrease to 20-40%

---

### Task 4: Monitor Brain State

1. Start recording
2. Subject performs different tasks:
   - Rest (2 min) → High Alpha
   - Mental math (2 min) → High Beta
   - Meditation (2 min) → High Theta
3. Stop and save
4. Analyze CSV data with external tools

---

## Troubleshooting

### Problem: Window doesn't open

**Solution:**
```bash
# Check if packages installed
pip list | grep PyQt5

# If missing, install
pip install PyQt5
```

---

### Problem: "COM port not found"

**Windows:**
1. Open Device Manager
2. Expand "Ports (COM & LPT)"
3. Find Arduino (COMx)
4. Update SERIAL_PORT in code

**Mac:**
```bash
ls /dev/tty.*
# Use /dev/tty.usbmodem*
```

**Linux:**
```bash
ls /dev/ttyUSB*
sudo chmod 666 /dev/ttyUSB0
```

---

### Problem: Plots not updating

**Cause:** Performance issue

**Solution:**
```python
# In code, increase update interval
UPDATE_INTERVAL = 100  # Change from 50 to 100ms
```

---

### Problem: "Module not found" error

**Solution:**
```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Tips for Best Results

### Hardware Mode
✓ Use shielded cables to reduce noise  
✓ Ensure good skin contact with electrodes  
✓ Minimize movement during recording  
✓ Record in quiet environment  
✓ Check ground connection  

### Simulation Mode
✓ Use for software testing  
✓ Great for demonstrations  
✓ Perfect for learning interface  

### General
✓ Close other programs for best performance  
✓ Use wired connection (not wireless) for Arduino  
✓ Save frequently during long sessions  
✓ Keep data organized with clear filenames  

---

## Next Steps

### Learn More
1. **WORKFLOW.md** - Detailed system operation
2. **DOCUMENTATION.md** - Technical API reference
3. **FLOWCHART.md** - Visual system diagrams
4. **INSTALLATION.md** - Detailed setup guide

### Customize
- Modify filter cutoff frequencies
- Change display update rates
- Add custom brain wave bands
- Export to different formats

### Extend
- Multi-channel support
- Real-time feedback
- Machine learning integration
- Cloud data upload

---

## Support

### Get Help
- **GitHub Issues**: Report bugs
- **Discussions**: Ask questions
- **Documentation**: Read full guides

### Contribute
- Fork the repository
- Submit pull requests
- Share improvements
- Report issues

---

## Quick Reference

### Key Files
- `codeV1.py` - Simulation mode
- `codeV2.py` - Arduino mode
- `requirements.txt` - Dependencies
- `README.md` - Main documentation

### Key Settings
```python
USE_ARDUINO = False    # Toggle mode
SERIAL_PORT = "COM3"   # Arduino port
SAMPLE_RATE = 1000     # Sampling frequency
BUFFER_SIZE = 2000     # 2-second window
LOWCUT = 1            # Filter low cutoff
HIGHCUT = 50          # Filter high cutoff
```

### Keyboard Shortcuts
- **Alt + F4**: Close application (Windows)
- **Cmd + Q**: Close application (Mac)

---

**Ready to start? Run `python codeV1.py` and begin monitoring!** 🧠⚡

---

*Last updated: December 5, 2025*
*Version: 1.0*
