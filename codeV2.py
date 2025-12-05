import sys
import serial
import numpy as np
from scipy.signal import butter, lfilter
from PyQt5 import QtWidgets, QtGui, QtCore as Qt
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from datetime import datetime

# -----------------------------
# USER SETTINGS
# -----------------------------
USE_ARDUINO = True     # Set to True if Arduino is connected
SERIAL_PORT = "COM5"    # Change for your system
BAUD_RATE = 9600
SAMPLE_RATE = 1000      # Arduino approximate sampling rate
BUFFER_SIZE = 2000      # Rolling window for time plot
UPDATE_INTERVAL = 50    # Update every 50ms instead of 1ms
DECIMATION = 10         # Process every Nth sample for display

LOWCUT = 1
HIGHCUT = 50
FILTER_ORDER = 4

# -----------------------------
# Bandpass Filter
# -----------------------------
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    return butter(order, [low, high], btype="band")

b, a = butter_bandpass(LOWCUT, HIGHCUT, SAMPLE_RATE, FILTER_ORDER)

def bandpass_filter(data):
    return lfilter(b, a, data)

# -----------------------------
# GUI Application
# -----------------------------
class EEG_GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NeuroViz Pro - Real-Time EEG Monitor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e27;
            }
            QLabel {
                color: #00d4ff;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton {
                background-color: #1a2332;
                color: #00d4ff;
                border: 2px solid #00d4ff;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00d4ff;
                color: #0a0e27;
            }
            QPushButton:pressed {
                background-color: #0099cc;
            }
            QGroupBox {
                color: #00d4ff;
                border: 2px solid #1e3a5f;
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)

        # Serial or simulation
        if USE_ARDUINO:
            try:
                self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
                self.use_simulation = False
                print("Connected to Arduino")
            except:
                print(f"Could not connect to {SERIAL_PORT}, using simulation")
                self.use_simulation = True
        else:
            self.ser = None
            self.use_simulation = True
            print("Running in simulation mode")

        # Data buffers
        self.data_buffer = np.zeros(BUFFER_SIZE)
        self.spec_buffer = np.zeros((200, 200))  # spectrogram image
        
        # Simulation and recording variables
        self.sim_time = 0
        self.is_recording = False
        self.recorded_data = []
        self.start_time = datetime.now()
        self.sample_count = 0
        self.avg_amplitude = 0
        self.max_amplitude = 0
        self.dominant_freq = 0
        self.update_counter = 0  # For decimation
        
        # Setup UI
        self.init_ui()

        # Timer for updates (50ms = 20 FPS, smooth and responsive)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(UPDATE_INTERVAL)

    def init_ui(self):
        """Initialize the enhanced user interface"""
        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Left side - Control Panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Right side - Visualization Panel
        viz_layout = QtWidgets.QVBoxLayout()
        
        # Header with status
        header = self.create_header()
        viz_layout.addWidget(header)
        
        # Configure PyQtGraph
        pg.setConfigOption('background', '#0a0e27')
        pg.setConfigOption('foreground', '#00d4ff')
        pg.setConfigOption('antialias', True)
        
        # Time-domain plot
        time_container = QtWidgets.QGroupBox("📊 REAL-TIME SIGNAL")
        time_layout = QtWidgets.QVBoxLayout()
        
        self.plot_time = pg.PlotWidget()
        self.plot_time.setYRange(-600, 600)
        self.plot_time.setLabel('left', 'Amplitude (μV)', color='#00d4ff')
        self.plot_time.setLabel('bottom', 'Samples', color='#00d4ff')
        self.plot_time.showGrid(x=True, y=True, alpha=0.3)
        self.curve_time = self.plot_time.plot(pen=pg.mkPen(color='#00ff88', width=2.5))
        
        time_layout.addWidget(self.plot_time)
        time_container.setLayout(time_layout)
        viz_layout.addWidget(time_container)

        # Bottom section - FFT and Spectrogram
        bottom_layout = QtWidgets.QHBoxLayout()
        
        # FFT plot
        fft_container = QtWidgets.QGroupBox("🎵 FREQUENCY ANALYSIS")
        fft_layout = QtWidgets.QVBoxLayout()
        
        self.plot_fft = pg.PlotWidget()
        self.plot_fft.setLabel('left', 'Power', color='#00d4ff')
        self.plot_fft.setLabel('bottom', 'Frequency (Hz)', color='#00d4ff')
        self.plot_fft.showGrid(x=True, y=True, alpha=0.3)
        self.plot_fft.setXRange(0, 100)
        self.curve_fft = self.plot_fft.plot(
            pen=pg.mkPen(color='#ff00ff', width=2.5),
            fillLevel=0, brush=(255, 0, 255, 80)
        )
        
        fft_layout.addWidget(self.plot_fft)
        
        fft_container.setLayout(fft_layout)
        bottom_layout.addWidget(fft_container)

        # Spectrogram
        spec_container = QtWidgets.QGroupBox("🌈 SPECTROGRAM")
        spec_layout = QtWidgets.QVBoxLayout()
        
        self.img = pg.ImageView()
        self.img.ui.roiBtn.hide()
        self.img.ui.menuBtn.hide()
        self.img.setColorMap(pg.colormap.get('viridis'))
        spec_layout.addWidget(self.img)
        
        spec_container.setLayout(spec_layout)
        bottom_layout.addWidget(spec_container)
        
        viz_layout.addLayout(bottom_layout)
        main_layout.addLayout(viz_layout, stretch=4)

    def create_header(self):
        """Create status header"""
        header = QtWidgets.QWidget()
        header.setStyleSheet("background-color: rgba(30, 58, 95, 0.6); border-radius: 10px; padding: 10px;")
        header_layout = QtWidgets.QHBoxLayout()
        
        title = QtWidgets.QLabel("⚡ NEUROVIZ PRO")
        title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #00ffff;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        status_text = "🟡 Simulation Mode" if self.use_simulation else "🟢 Arduino Connected"
        self.status_label = QtWidgets.QLabel(status_text)
        self.status_label.setStyleSheet("font-size: 14pt; color: #00ff88;")
        header_layout.addWidget(self.status_label)
        
        self.time_label = QtWidgets.QLabel("00:00:00")
        self.time_label.setStyleSheet("font-size: 14pt; color: #00d4ff;")
        header_layout.addWidget(self.time_label)
        
        header.setLayout(header_layout)
        return header

    def create_control_panel(self):
        """Create control panel"""
        panel = QtWidgets.QWidget()
        panel.setMaximumWidth(350)
        panel.setStyleSheet("background-color: rgba(20, 30, 50, 0.7); border-radius: 15px; padding: 15px;")
        
        layout = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("CONTROL CENTER")
        title.setAlignment(Qt.Qt.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #00ffff; padding: 15px;")
        layout.addWidget(title)
        
        # Statistics
        stats_group = QtWidgets.QGroupBox("📈 Live Statistics")
        stats_layout = QtWidgets.QVBoxLayout()
        
        self.stat_samples = QtWidgets.QLabel("Samples: 0")
        self.stat_avg = QtWidgets.QLabel("Avg: 0 μV")
        self.stat_max = QtWidgets.QLabel("Max: 0 μV")
        self.stat_freq = QtWidgets.QLabel("Freq: 0 Hz")
        
        for label in [self.stat_samples, self.stat_avg, self.stat_max, self.stat_freq]:
            label.setStyleSheet("font-size: 13pt; padding: 8px;")
            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Controls
        controls_group = QtWidgets.QGroupBox("🎮 Controls")
        controls_layout = QtWidgets.QVBoxLayout()
        
        self.record_btn = QtWidgets.QPushButton("● START RECORDING")
        self.record_btn.clicked.connect(self.toggle_recording)
        controls_layout.addWidget(self.record_btn)
        
        self.save_btn = QtWidgets.QPushButton("💾 SAVE DATA")
        self.save_btn.clicked.connect(self.save_data)
        self.save_btn.setEnabled(False)
        controls_layout.addWidget(self.save_btn)
        
        self.clear_btn = QtWidgets.QPushButton("🔄 CLEAR")
        self.clear_btn.clicked.connect(self.clear_buffer)
        controls_layout.addWidget(self.clear_btn)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel


    def toggle_recording(self):
        """Toggle recording"""
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.record_btn.setText("⏹ STOP RECORDING")
            self.recorded_data = []
            self.save_btn.setEnabled(False)
        else:
            self.record_btn.setText("● START RECORDING")
            self.save_btn.setEnabled(True)

    def save_data(self):
        """Save recorded data"""
        if not self.recorded_data:
            return
        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Data", f"eeg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if filename:
            np.savetxt(filename, self.recorded_data, delimiter=',')

    def clear_buffer(self):
        """Clear buffers"""
        self.data_buffer = np.zeros(BUFFER_SIZE)
        self.spec_buffer = np.zeros((200, 200))
        self.sample_count = 0

    # ------------------------------------
    # Update plots
    # ------------------------------------
    def update(self):
        """Update all plots and statistics (optimized)"""
        # Process multiple samples per update for smooth simulation
        samples_per_update = UPDATE_INTERVAL  # Process 50 samples per 50ms update
        
        for _ in range(samples_per_update):
            # Get data
            if self.use_simulation:
                self.sim_time += 1
                # Enhanced brain wave simulation
                t = self.sim_time / SAMPLE_RATE
                delta = 80 * np.sin(2 * np.pi * 2 * t)
                theta = 100 * np.sin(2 * np.pi * 6 * t)
                alpha = 200 * np.sin(2 * np.pi * 10 * t)
                beta = 120 * np.sin(2 * np.pi * 20 * t)
                gamma = 60 * np.sin(2 * np.pi * 35 * t)
                noise = np.random.randn() * 32
                value = 512 + delta + theta + alpha + beta + gamma + noise
            else:
                try:
                    raw = self.ser.readline().decode().strip()
                    value = int(raw)
                except:
                    return

            self.sample_count += 1
            
            if self.is_recording:
                self.recorded_data.append([self.sample_count, value])

            # Update buffer (faster without roll)
            self.data_buffer[:-1] = self.data_buffer[1:]
            self.data_buffer[-1] = value
        
        # Only update visuals after processing all samples
        self.update_counter += 1
        if self.update_counter % 2 != 0:  # Update plots every other cycle (10 FPS)
            return

        # Filter (only once per visual update)
        filtered = bandpass_filter(self.data_buffer)

        # Statistics (use cached values for performance)
        recent_data = filtered[-200:]
        self.avg_amplitude = np.mean(np.abs(recent_data))
        self.max_amplitude = np.max(np.abs(recent_data))
        
        # TIME PLOT - Decimate for display (show every Nth point)
        decimated_filtered = filtered[::DECIMATION]
        self.curve_time.setData(decimated_filtered)

        # FFT (reduce resolution for performance)
        freqs = np.fft.rfftfreq(BUFFER_SIZE, d=1.0 / SAMPLE_RATE)
        fft_vals = np.abs(np.fft.rfft(filtered))
        
        if len(fft_vals) > 1:
            dom_idx = np.argmax(fft_vals[1:100]) + 1
            self.dominant_freq = freqs[dom_idx]
        
        # Show only relevant frequency range (0-100 Hz) with decimation
        freq_limit = 100
        freq_indices = freqs < freq_limit
        display_freqs = freqs[freq_indices][::2]  # Decimate by 2
        display_fft = fft_vals[freq_indices][::2]
        self.curve_fft.setData(display_freqs, display_fft)

        # SPECTROGRAM (update less frequently, most expensive operation)
        if self.update_counter % 3 == 0:  # Update every 3rd cycle
            fft_line = fft_vals[:200]
            # Faster than roll
            self.spec_buffer[:-1] = self.spec_buffer[1:]
            self.spec_buffer[-1, :] = fft_line
            self.img.setImage(self.spec_buffer.T, autoLevels=False, levels=(0, 500))

        # Update UI labels (only every 10th cycle to reduce overhead)
        if self.update_counter % 10 == 0:
            elapsed = datetime.now() - self.start_time
            self.time_label.setText(str(elapsed).split('.')[0])
            self.stat_samples.setText(f"Samples: {self.sample_count:,}")
            self.stat_avg.setText(f"Avg: {self.avg_amplitude:.1f} μV")
            self.stat_max.setText(f"Max: {self.max_amplitude:.1f} μV")
            self.stat_freq.setText(f"Freq: {self.dominant_freq:.1f} Hz")

    # Close serial on exit
    def closeEvent(self, event):
        if self.ser is not None:
            self.ser.close()
        event.accept()


# -----------------------------
# Run App
# -----------------------------
app = QtWidgets.QApplication(sys.argv)
window = EEG_GUI()
window.show()
sys.exit(app.exec_())
