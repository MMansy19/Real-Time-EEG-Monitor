# Technical Documentation - NeuroViz Pro

## API Reference

### Core Classes

#### `EEG_GUI(QtWidgets.QMainWindow)`

Main application class that handles the GUI and signal processing.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `use_simulation` | bool | True if using synthetic data, False if Arduino |
| `ser` | serial.Serial | Serial port object for Arduino communication |
| `data_buffer` | np.ndarray | Rolling buffer of raw samples (size: BUFFER_SIZE) |
| `spec_buffer` | np.ndarray | 2D spectrogram data array (200×200) |
| `recorded_data` | list | List of [sample_num, value] pairs during recording |
| `is_recording` | bool | Recording state flag |
| `sample_count` | int | Total samples acquired since start |
| `sim_time` | int | Current simulation time step |
| `avg_amplitude` | float | Average signal amplitude (μV) |
| `max_amplitude` | float | Maximum signal amplitude (μV) |
| `dominant_freq` | float | Peak frequency in spectrum (Hz) |

**Methods:**

##### `__init__(self)`
Initialize the application window and configure mode.

```python
def __init__(self):
    super().__init__()
    self.setWindowTitle("NeuroViz Pro - Real-Time EEG Monitor")
    self.setGeometry(100, 100, 1400, 900)
    # ... initialize serial/simulation ...
```

**Returns:** None

---

##### `init_ui(self)`
Create and layout all GUI components.

```python
def init_ui(self):
    """Initialize the user interface layout"""
```

**Components Created:**
- Header with status and timer
- Control panel with buttons
- Time-domain plot
- FFT spectrum plot
- Spectrogram display
- Band power indicators
- Statistics labels

**Returns:** None

---

##### `update(self)`
Main update loop called every UPDATE_INTERVAL milliseconds.

```python
def update(self):
    """Update all plots and statistics (optimized)"""
```

**Processing Steps:**
1. Acquire samples (50 per cycle)
2. Update data buffer
3. Apply bandpass filter
4. Compute FFT
5. Update visualizations
6. Calculate band powers
7. Update statistics

**Returns:** None

---

##### `toggle_recording(self)`
Start or stop data recording.

```python
def toggle_recording(self):
    """Toggle recording state"""
```

**Behavior:**
- If OFF → ON: Clear `recorded_data`, disable save button
- If ON → OFF: Enable save button, keep data in memory

**Returns:** None

---

##### `save_data(self)`
Export recorded data to CSV file.

```python
def save_data(self):
    """Save recorded data to CSV"""
```

**CSV Format:**
```
sample_number,value
1,512.34
2,515.67
...
```

**Returns:** None

---

##### `clear_buffer(self)`
Reset all data buffers and counters.

```python
def clear_buffer(self):
    """Clear all buffers"""
```

**Resets:**
- `data_buffer` → zeros
- `spec_buffer` → zeros
- `sample_count` → 0

**Returns:** None

---

### Utility Functions

#### `butter_bandpass(lowcut, highcut, fs, order=4)`

Design a Butterworth bandpass filter.

**Parameters:**
- `lowcut` (float): Low cutoff frequency in Hz
- `highcut` (float): High cutoff frequency in Hz
- `fs` (float): Sampling frequency in Hz
- `order` (int): Filter order (default: 4)

**Returns:** tuple (b, a) - Filter coefficients

**Example:**
```python
b, a = butter_bandpass(1, 50, 1000, order=4)
```

---

#### `bandpass_filter(data)`

Apply the pre-designed bandpass filter to data.

**Parameters:**
- `data` (np.ndarray): Input signal array

**Returns:** np.ndarray - Filtered signal

**Example:**
```python
filtered = bandpass_filter(raw_signal)
```

---

## Configuration Reference

### Global Constants

#### Signal Processing

| Constant | Default | Unit | Description |
|----------|---------|------|-------------|
| `SAMPLE_RATE` | 1000 | Hz | ADC sampling frequency |
| `BUFFER_SIZE` | 2000 | samples | Rolling window size (2 seconds) |
| `LOWCUT` | 1 | Hz | Highpass filter cutoff |
| `HIGHCUT` | 50 | Hz | Lowpass filter cutoff |
| `FILTER_ORDER` | 4 | - | Butterworth filter order |

#### Display

| Constant | Default | Unit | Description |
|----------|---------|------|-------------|
| `UPDATE_INTERVAL` | 50 | ms | GUI refresh rate |
| `DECIMATION` | 10 | - | Display point reduction factor |

#### Hardware

| Constant | Default | Description |
|----------|---------|-------------|
| `USE_ARDUINO` | False | Enable/disable hardware mode |
| `SERIAL_PORT` | "COM3" | Serial port identifier |
| `BAUD_RATE` | 9600 | Serial communication speed |

---

## Data Structures

### Recorded Data Format

**Type:** List of lists

**Structure:**
```python
[
    [sample_number, value],
    [1, 512.34],
    [2, 515.67],
    ...
]
```

**CSV Export:**
```csv
Sample,Value
1,512.34
2,515.67
```

---

### Buffer Arrays

#### Time-Domain Buffer

**Type:** `np.ndarray`  
**Shape:** `(BUFFER_SIZE,)` = `(2000,)`  
**Data Type:** `float64`  
**Contents:** Raw ADC values (0-1023 for Arduino, simulated range)

#### Spectrogram Buffer

**Type:** `np.ndarray`  
**Shape:** `(200, 200)`  
**Data Type:** `float64`  
**Contents:** Time-frequency magnitude data

**Layout:**
- Rows: Time (200 windows)
- Columns: Frequency bins (0-100 Hz)
- Values: FFT magnitude

---

## Signal Processing Algorithms

### Bandpass Filter Design

**Algorithm:** Butterworth IIR Filter

**Transfer Function:**
$$H(s) = \frac{1}{\sqrt{1 + \left(\frac{\omega}{\omega_c}\right)^{2n}}}$$

Where:
- $\omega_c$ = cutoff frequency
- $n$ = filter order

**Implementation:**
```python
nyquist = 0.5 * SAMPLE_RATE  # 500 Hz
low = LOWCUT / nyquist        # 1/500 = 0.002
high = HIGHCUT / nyquist      # 50/500 = 0.1
b, a = butter(FILTER_ORDER, [low, high], btype='band')
```

**Frequency Response:**
- Passband: 1-50 Hz
- Stopband attenuation: ~24 dB/octave (4th order)
- Phase: Non-linear (IIR characteristic)

---

### FFT Analysis

**Algorithm:** Fast Fourier Transform (Cooley-Tukey)

**Parameters:**
- Input: 2000 samples (filtered signal)
- Output: 1001 frequency bins (0-500 Hz)
- Resolution: 500/1001 ≈ 0.5 Hz per bin

**Implementation:**
```python
freqs = np.fft.rfftfreq(BUFFER_SIZE, d=1/SAMPLE_RATE)
fft_vals = np.abs(np.fft.rfft(filtered_signal))
```

**Computation:**
$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j2\pi kn/N}$$

---

### Band Power Calculation

**Method:** Frequency-domain integration

**Bands:**

| Band | Range (Hz) | Bin Indices |
|------|------------|-------------|
| Delta (δ) | 0.5 - 4 | 1 - 8 |
| Theta (θ) | 4 - 8 | 8 - 16 |
| Alpha (α) | 8 - 13 | 16 - 26 |
| Beta (β) | 13 - 30 | 26 - 60 |
| Gamma (γ) | 30 - 50 | 60 - 100 |

**Algorithm:**
```python
for low, high in band_ranges:
    mask = (freqs >= low) & (freqs <= high)
    band_power = np.sum(fft_vals[mask])
    percentage = (band_power / total_power) * 100
```

**Formula:**
$$P_{band} = \sum_{f=f_{low}}^{f_{high}} |X[f]|^2$$

$$\%_{band} = \frac{P_{band}}{\sum_{bands} P_{band}} \times 100$$

---

## Performance Optimization

### Update Cycle Optimization

**Strategy:** Staggered updates to reduce CPU load

| Component | Update Frequency | Cycle Modulo |
|-----------|------------------|--------------|
| Data acquisition | Every cycle (50ms) | N/A |
| Time plot | Every 2 cycles (100ms) | `% 2 == 0` |
| FFT plot | Every 2 cycles (100ms) | `% 2 == 0` |
| Spectrogram | Every 3 cycles (150ms) | `% 3 == 0` |
| Band powers | Every 5 cycles (250ms) | `% 5 == 0` |
| Statistics text | Every 10 cycles (500ms) | `% 10 == 0` |

**CPU Usage Reduction:** ~60-70% compared to updating all every cycle

---

### Display Decimation

**Time Plot Decimation:**
```python
decimated = filtered[::DECIMATION]  # Every 10th point
# 2000 samples → 200 display points
```

**Benefits:**
- Reduced rendering overhead
- Smoother animation
- Lower memory bandwidth

**FFT Decimation:**
```python
display_freqs = freqs[::2]   # Every 2nd frequency
display_fft = fft_vals[::2]
# 1001 bins → 500 display points
```

---

### Memory Management

**Buffer Updating:**
```python
# Efficient (no reallocation)
buffer[:-1] = buffer[1:]
buffer[-1] = new_value

# Inefficient (creates new array)
buffer = np.roll(buffer, -1)  # AVOID
```

**Spectrogram Rolling:**
```python
# Efficient
spec_buffer[:-1] = spec_buffer[1:]
spec_buffer[-1, :] = fft_line
```

---

## Error Handling

### Serial Port Errors

**Scenario:** Arduino disconnected during operation

**Handling:**
```python
try:
    raw = self.ser.readline().decode().strip()
    value = int(raw)
except:
    return  # Skip update cycle
```

**Behavior:** Silently skip bad samples, continue operation

---

### Data Validation

**Arduino Value Range:**
```python
# Expected: 0-1023 (10-bit ADC)
if 0 <= value <= 1023:
    process(value)
else:
    log_error(f"Invalid value: {value}")
```

**Simulation Bounds:**
```python
# Ensure reasonable range
value = np.clip(simulated_value, 0, 1023)
```

---

## Testing

### Unit Test Examples

#### Filter Test
```python
def test_bandpass_filter():
    # Generate test signal
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2*np.pi*10*t)  # 10 Hz sine
    
    # Apply filter
    filtered = bandpass_filter(signal)
    
    # Verify passband
    fft = np.abs(np.fft.rfft(filtered))
    freqs = np.fft.rfftfreq(len(signal), 1/1000)
    peak_freq = freqs[np.argmax(fft)]
    
    assert 9 < peak_freq < 11  # 10 Hz within tolerance
```

#### FFT Test
```python
def test_fft_resolution():
    # 2000 samples at 1000 Hz
    freqs = np.fft.rfftfreq(2000, 1/1000)
    
    # Check resolution
    resolution = freqs[1] - freqs[0]
    assert 0.49 < resolution < 0.51  # ~0.5 Hz
```

---

## Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `numpy` | ≥1.20.0 | Numerical computations |
| `scipy` | ≥1.7.0 | Signal processing (butter, lfilter) |
| `PyQt5` | ≥5.15.0 | GUI framework |
| `pyqtgraph` | ≥0.12.0 | Real-time plotting |
| `pyserial` | ≥3.5 | Arduino communication |

### Installation
```bash
pip install numpy>=1.20.0 scipy>=1.7.0 PyQt5>=5.15.0 pyqtgraph>=0.12.0 pyserial>=3.5
```

---

## Troubleshooting Guide

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add to update() method
logging.debug(f"Sample: {value}, Filtered: {filtered[-1]}")
```

### Performance Profiling

```python
import time

def update(self):
    start = time.time()
    
    # ... processing ...
    
    elapsed = time.time() - start
    if elapsed > 0.05:  # Warn if > 50ms
        print(f"⚠ Slow update: {elapsed*1000:.1f}ms")
```

### Memory Usage

```python
import sys

print(f"Buffer size: {sys.getsizeof(self.data_buffer)} bytes")
print(f"Recorded size: {sys.getsizeof(self.recorded_data)} bytes")
```

---

## Advanced Customization

### Custom Filter Design

```python
# Example: Notch filter at 50 Hz (power line interference)
from scipy.signal import iirnotch

b_notch, a_notch = iirnotch(50, Q=30, fs=1000)

def apply_notch(data):
    return lfilter(b_notch, a_notch, data)
```

### Custom Brain Wave Bands

```python
# Define new bands
CUSTOM_BANDS = {
    'slow_wave': (0.5, 2),
    'delta': (2, 4),
    'theta': (4, 8),
    'alpha_low': (8, 10),
    'alpha_high': (10, 13),
    'beta': (13, 30),
    'gamma': (30, 100)
}
```

### Export to Other Formats

```python
# Export to NumPy binary
np.save('eeg_recording.npy', self.recorded_data)

# Export to MATLAB format
from scipy.io import savemat
savemat('eeg_recording.mat', {'data': self.recorded_data})
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-05 | Initial release |
| 1.1 | TBD | Performance improvements |
| 2.0 | TBD | Multi-channel support |

---

*For more information, see README.md and WORKFLOW.md*
