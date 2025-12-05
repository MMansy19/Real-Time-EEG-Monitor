# System Flowchart - NeuroViz Pro

## Overview

This document provides visual flowcharts for the NeuroViz Pro EEG monitoring system, including the two operation modes (Arduino and Simulation) and the complete signal processing pipeline.

---

## Main System Flowchart

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION START                              │
│                         python codeV1.py / codeV2.py                    │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   Read Configuration         │
                    │   USE_ARDUINO = True/False   │
                    └──────────┬───────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
    ┌───────────────────────┐    ┌───────────────────────┐
    │   USE_ARDUINO = FALSE │    │   USE_ARDUINO = TRUE  │
    │   SIMULATION MODE     │    │   ARDUINO MODE        │
    └───────────┬───────────┘    └───────────┬───────────┘
                │                             │
                │                    ┌────────▼────────────┐
                │                    │ Try Serial.open()   │
                │                    │ Port: SERIAL_PORT   │
                │                    │ Baud: 9600          │
                │                    └────────┬────────────┘
                │                         ┌───┴───┐
                │                         │       │
                │                    ┌────▼───┐ ┌─▼──────┐
                │                    │SUCCESS │ │ FAILED │
                │                    └────┬───┘ └─┬──────┘
                │                         │       │
                │                         │    ┌──▼─────────────┐
                │                         │    │ Print Warning  │
                │                         │    │ Fallback to    │
                │                         │    │ Simulation     │
                │                         │    └──┬─────────────┘
                │                         │       │
                └─────────────────────────┴───────┘
                                   │
                        ┌──────────▼──────────┐
                        │   Initialize GUI    │
                        │   • Create window   │
                        │   • Setup plots     │
                        │   • Create buttons  │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │  Initialize Buffers │
                        │  • data_buffer[2000]│
                        │  • spec_buffer      │
                        │  • recorded_data[]  │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │   Start Timer       │
                        │   Interval: 50ms    │
                        │   Connect: update() │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼───────────────┐
                        │   MAIN EVENT LOOP        │
                        │   (Qt Application Loop)  │
                        └──────────┬───────────────┘
                                   │
                              ┌────▼────┐
                              │ Timer   │
                              │ Fired?  │
                              └────┬────┘
                                   │
                              ┌────▼────────────┐
                              │  update()       │
                              │  Every 50ms     │
                              └────┬────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐        ┌──────────────────┐      ┌─────────────────┐
│ DATA          │        │ SIGNAL           │      │ VISUALIZATION   │
│ ACQUISITION   │───────>│ PROCESSING       │─────>│ & UI UPDATE     │
│ (50 samples)  │        │ (Filter, FFT)    │      │ (Plots, Stats)  │
└───────┬───────┘        └──────────────────┘      └─────────────────┘
        │
        ▼
┌───────────────────┐
│ RECORDING?        │
└───────┬───────────┘
        │
    ┌───┴────┐
    │        │
    ▼        ▼
┌────────┐ ┌─────┐
│  SAVE  │ │SKIP │
└────────┘ └─────┘
```

---

## Dual Mode Operation Flowchart

```
                    ┌─────────────────────────────┐
                    │    APPLICATION LAUNCH       │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Check USE_ARDUINO  │
                    └──────────┬──────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
┌───────────▼───────────┐            ┌────────────▼──────────┐
│   MODE 1: SIMULATION  │            │  MODE 2: ARDUINO      │
│   USE_ARDUINO = False │            │  USE_ARDUINO = True   │
└───────────┬───────────┘            └────────────┬──────────┘
            │                                     │
            │                            ┌────────▼────────┐
            │                            │ Serial.open()   │
            │                            │ Port: COMx      │
            │                            └────────┬────────┘
            │                                 ┌───┴────┐
            │                                 │        │
            │                            ┌────▼───┐ ┌─▼──────┐
            │                            │SUCCESS │ │ FAIL   │
            │                            └────┬───┘ └─┬──────┘
            │                                 │       │
            │                                 │    ┌──▼────────┐
            │                                 │    │ Fallback  │
            │                                 │    │    to     │
            │                                 │    │Simulation │
            │                                 │    └──┬────────┘
            │                                 │       │
            └─────────────────────────────────┴───────┘
                                     │
                        ┌────────────▼────────────┐
                        │   DATA GENERATION       │
                        └────────────┬────────────┘
                                     │
            ┌────────────────────────┴────────────────────────┐
            │                                                 │
┌───────────▼──────────┐                        ┌─────────────▼──────────┐
│ SIMULATION SOURCE    │                        │ HARDWARE SOURCE        │
│                      │                        │                        │
│ t = time/1000        │                        │ while serial.available:│
│ δ = 20*sin(2π*2*t)  │                        │   line = readline()    │
│ θ = 25*sin(2π*6*t)  │                        │   value = int(line)    │
│ α = 50*sin(2π*10*t) │                        │   validate(value)      │
│ β = 30*sin(2π*20*t) │                        │                        │
│ γ = 15*sin(2π*35*t) │                        │ ADC Range: 0-1023      │
│ noise = N(0, 8)      │                        │ Sampling: 1000 Hz      │
│                      │                        │                        │
│ value = 512 + Σ      │                        │                        │
│                      │                        │                        │
│ ADVANTAGES:          │                        │ ADVANTAGES:            │
│ • No hardware needed │                        │ • Real physiological   │
│ • Controlled signal  │                        │ • Clinical research    │
│ • Fast testing       │                        │ • Subject monitoring   │
│ • Education          │                        │                        │
└───────────┬──────────┘                        └─────────────┬──────────┘
            │                                                 │
            └────────────────────────┬────────────────────────┘
                                     │
                        ┌────────────▼────────────┐
                        │    COMMON PROCESSING    │
                        │    • Buffering          │
                        │    • Filtering          │
                        │    • FFT Analysis       │
                        │    • Band Calculation   │
                        │    • Visualization      │
                        └─────────────────────────┘
```

---

## Data Acquisition Pipeline (Mode-Specific)

### Arduino Mode Pipeline

```
┌─────────────────┐
│  Arduino Board  │
│  • EEG Sensor   │
│  • ADC (10-bit) │
│  • Serial TX    │
└────────┬────────┘
         │ USB Cable
         ▼
┌─────────────────┐
│  Computer       │
│  Serial Port    │
│  (COMx/ttyUSBx) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PySerial       │
│  • Open port    │
│  • 9600 baud    │
│  • Read line    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parse Data     │
│  • Decode UTF-8 │
│  • Strip \n     │
│  • int(value)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validation     │
│  • Range check  │
│  • Error handle │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Buffer    │
└─────────────────┘
```

### Simulation Mode Pipeline

```
┌─────────────────┐
│  Time Counter   │
│  sim_time++     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Calculate t    │
│  t = cnt / 1000 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate Bands │
│  • Delta: 2 Hz  │
│  • Theta: 6 Hz  │
│  • Alpha: 10 Hz │
│  • Beta: 20 Hz  │
│  • Gamma: 35 Hz │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Add Noise      │
│  N(0, 8)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Combine Signal │
│  val = 512 + Σ  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Buffer    │
└─────────────────┘
```

---

## Signal Processing Pipeline

```
┌─────────────────────────────────────────────────────────┐
│               RAW DATA BUFFER (2000 samples)            │
│                   [512, 515, 510, ...]                  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  BANDPASS FILTER     │
              │  Butterworth 4th     │
              │  1-50 Hz             │
              └──────────┬───────────┘
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
   ┌────────────────┐       ┌────────────────┐
   │  TIME DOMAIN   │       │  FFT TRANSFORM │
   │  • Decimate    │       │  • 2000 → 1001 │
   │  • Display     │       │  • 0-500 Hz    │
   └────────────────┘       └────────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
          ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
          │ DOMINANT    │  │ BAND POWER  │  │ SPECTROGRAM  │
          │ FREQUENCY   │  │ ANALYSIS    │  │ HEATMAP      │
          │             │  │             │  │              │
          │ Peak in FFT │  │ δ: 0.5-4 Hz │  │ Time-Freq    │
          │ 1-100 Hz    │  │ θ: 4-8 Hz   │  │ 2D Array     │
          │             │  │ α: 8-13 Hz  │  │ Rolling      │
          │ Result:     │  │ β: 13-30 Hz │  │ Update       │
          │ 10.2 Hz     │  │ γ: 30-50 Hz │  │              │
          └─────────────┘  └─────────────┘  └──────────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
                                     ▼
                          ┌──────────────────┐
                          │  UPDATE GUI      │
                          │  • Plots         │
                          │  • Statistics    │
                          │  • Band %        │
                          └──────────────────┘
```

---

## User Interaction Flowchart

```
                    ┌──────────────────┐
                    │  APPLICATION     │
                    │  RUNNING         │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  User Watching   │
                    │  Live Displays   │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  User Action?    │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌──────────────┐
│ Click START   │    │ Click CLEAR   │    │ Click SAVE   │
│ RECORDING     │    │ BUFFER        │    │ DATA         │
└───────┬───────┘    └───────┬───────┘    └──────┬───────┘
        │                    │                    │
        ▼                    ▼                    │
┌───────────────┐    ┌───────────────┐           │
│ recording=True│    │ Reset all     │           │
│ Clear buffer  │    │ buffers       │           │
│ Disable save  │    │ count=0       │           │
└───────┬───────┘    └───────────────┘           │
        │                                         │
        ▼                                         │
┌───────────────┐                                 │
│ Collect data  │                                 │
│ in memory     │                                 │
└───────┬───────┘                                 │
        │                                         │
        ▼                                         │
┌───────────────┐                                 │
│ Click STOP    │                                 │
│ RECORDING     │                                 │
└───────┬───────┘                                 │
        │                                         │
        ▼                                         │
┌───────────────┐                                 │
│recording=False│                                 │
│ Enable save   │                                 │
└───────┬───────┘                                 │
        │                                         │
        └─────────────────────┬───────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ File Dialog      │
                    │ Choose name      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Export to CSV    │
                    │ eeg_YYYYMMDD.csv │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Success Message  │
                    │ Continue Monitor │
                    └──────────────────┘
```

---

## Performance Optimization Flow

```
┌───────────────────────────────────────────────────────┐
│              UPDATE CYCLE (Every 50ms)                │
└─────────────────────────┬─────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│ ACQUISITION      │            │ UPDATE COUNTER   │
│ Loop 50 times    │            │ counter++        │
│ Get 50 samples   │            └────────┬─────────┘
└──────────────────┘                     │
          │                              │
          ▼                              ▼
┌──────────────────┐            ┌──────────────────┐
│ BUFFER UPDATE    │            │ CONDITIONAL      │
│ Roll buffer      │            │ UPDATES          │
│ Append new data  │            └────────┬─────────┘
└──────────────────┘                     │
                                         │
                        ┌────────────────┼────────────────┐
                        │                │                │
                        ▼                ▼                ▼
              ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
              │ if % 2 == 0 │  │ if % 3 == 0 │  │ if % 5 == 0 │
              │ Update:     │  │ Update:     │  │ Update:     │
              │ • Time plot │  │ • Specgram  │  │ • Bands %   │
              │ • FFT plot  │  │             │  │             │
              │ (100ms)     │  │ (150ms)     │  │ (250ms)     │
              └─────────────┘  └─────────────┘  └─────────────┘
                        │                │                │
                        └────────────────┼────────────────┘
                                         │
                                         ▼
                              ┌──────────────────┐
                              │ if % 10 == 0     │
                              │ Update:          │
                              │ • Statistics     │
                              │ • Timer          │
                              │ (500ms)          │
                              └──────────────────┘

RESULT: 60-70% CPU reduction compared to updating everything every cycle
```

---

## Complete System State Diagram

```
                    ┌──────────────┐
                    │  INIT STATE  │
                    │ • Setup GUI  │
                    │ • Open port  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  IDLE STATE  │
                    │ • Monitoring │
                    │ • No record  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
      ┌──────────┐  ┌──────────┐  ┌─────────┐
      │RECORDING │  │ CLEARING │  │ SAVING  │
      │  STATE   │  │  STATE   │  │  STATE  │
      └────┬─────┘  └────┬─────┘  └────┬────┘
           │             │             │
           └─────────────┼─────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Back to IDLE │
                  └──────────────┘
```

---

## Legend

```
┌─────────┐
│ Process │  = Action or computation
└─────────┘

┌─────────┐
│Decision?│  = Conditional branch
└─────────┘

    │
    ▼         = Data flow direction

─────────────  = Parallel execution

═════════════  = Critical path
```

---

## Key Takeaways

### Two Modes Operation
1. **Simulation Mode**: Software-only, no hardware required
2. **Arduino Mode**: Real sensor data with automatic fallback

### Performance Strategy
- Staggered updates (2x, 3x, 5x, 10x cycles)
- Display decimation (10:1 ratio)
- Selective processing based on necessity

### Data Flow
Raw → Buffer → Filter → FFT → Analysis → Display

### User Interaction
Simple button controls for record/save/clear operations

---

*For detailed code implementation, see codeV1.py and codeV2.py*
*For workflow details, see WORKFLOW.md*
