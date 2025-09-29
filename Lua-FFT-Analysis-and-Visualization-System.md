# Lua FFT Analysis and Visualization System

## Project Overview
Create a demonstration system for Fourier analysis on a Lua-based microcontroller with visualization capabilities using LÖVE2D framework.

## Technical Requirements

### FFT Libraries
- **Primary**: LuaFFT (pure Lua implementation)
- **Secondary**: lua-fftw3 bindings (optional, for performance)
- Support fallback between libraries based on availability

### Core Functionality

#### 1. Signal Generation Module
Create functions to generate test signals:
- Pure sine waves (single frequency)
- Complex periodic signals (sum of multiple frequencies)
- Square wave
- Sawtooth wave
- Triangle wave
- Custom waveform input from microcontroller sensors

Parameters to control:
- Frequency (Hz)
- Amplitude
- Phase offset
- Sample rate
- Number of samples

#### 2. FFT Processing Module
Implement FFT analysis with:
- Real-to-complex FFT
- Inverse FFT capability
- Window functions (Hamming, Hanning, Blackman) to reduce spectral leakage
- Frequency bin calculation
- Magnitude and phase extraction
- Power spectral density calculation
- **Fourier series coefficients calculation**:
  - Extract DC component (a₀)
  - Calculate cosine coefficients (aₙ) for each harmonic
  - Calculate sine coefficients (bₙ) for each harmonic
  - Convert between trigonometric form (aₙ, bₙ) and exponential form (cₙ)
  - Compute amplitude (Aₙ) and phase (φₙ) for each harmonic
  - Support both real and complex coefficient representations
  - Calculate coefficients for arbitrary number of harmonics

Handle:
- Different buffer sizes (128, 256, 512, 1024, 2048 samples)
- Zero-padding for non-power-of-2 sizes
- Normalization of results
- Period detection for non-integer period signals
- Coefficient precision and numerical stability

#### 3. Fourier Series Reconstruction
Implement classical Fourier series:
- Calculate coefficients (a₀, aₙ, bₙ)
- Reconstruct signal from N harmonics
- Show convergence as more terms are added
- Display Gibbs phenomenon near discontinuities

#### 4. LÖVE2D Visualization

##### Display Components:
1. **Time Domain Plot**
   - Original signal waveform
   - X-axis: Time (seconds or samples)
   - Y-axis: Amplitude
   - Grid and axis labels
   - Real-time scrolling for live data

2. **Frequency Domain Plot (Spectrum)**
   - FFT magnitude spectrum
   - X-axis: Frequency (Hz)
   - Y-axis: Magnitude (dB or linear)
   - Color-coded peaks
   - Logarithmic option for frequency axis
   - Peak detection and labeling

3. **Waterfall/Spectrogram View**
   - Time on Y-axis (scrolling down)
   - Frequency on X-axis
   - Color intensity represents magnitude
   - Historical view of frequency content

4. **Fourier Series Decomposition**
   - Show individual harmonic components
   - Animated addition of terms
   - Side-by-side comparison: original vs. reconstruction
   - Error visualization

5. **Phase Plot**
   - Phase spectrum
   - Unwrapped phase option

##### Interactive Controls:
- Adjust number of FFT points
- Change window function
- Toggle between log/linear scales
- Zoom and pan on plots
- Select different signal sources
- Control animation speed for Fourier series buildup
- Export data/screenshots

##### Visual Style:
- Dark background (easier on eyes, better for demos)
- Bright, contrasting colors for signals
- Grid lines with subtle transparency
- Smooth anti-aliased rendering
- Professional scientific visualization aesthetic
- FPS and performance metrics display

### Microcontroller Integration

#### Data Input Options:
1. **Simulated signals** (for testing)
2. **ADC input** from microcontroller sensors:
   - Audio input (microphone)
   - Vibration sensors
   - Temperature variations
   - Any periodic sensor data
3. **Serial communication** for real-time data streaming
4. **File-based input** for pre-recorded data

#### Performance Considerations:
- Efficient memory management for embedded systems
- Configurable FFT size based on available RAM
- Downsampling options for high-rate sensors
- Buffer management for streaming data
- Frame rate optimization in LÖVE2D

### Code Architecture

```
project/
├── main.lua                 # LÖVE2D entry point
├── fourier/
│   ├── init.lua            # FFT module loader
│   ├── luafft_wrapper.lua  # LuaFFT implementation
│   └── fftw3_wrapper.lua   # FFTW3 bindings (optional)
├── signal/
│   ├── generator.lua       # Signal generation functions
│   └── fourier_series.lua  # Fourier series computation
├── visualization/
│   ├── plot.lua            # Generic plotting utilities
│   ├── spectrum.lua        # Frequency spectrum display
│   ├── waveform.lua        # Time-domain waveform display
│   └── spectrogram.lua     # Waterfall/spectrogram view
├── ui/
│   └── controls.lua        # Interactive UI elements
└── hardware/
    └── input.lua           # Microcontroller data interface
```

### Example Use Cases

#### Demo 1: Pure Tone Analysis
- Generate 440 Hz sine wave (A4 note)
- Show single peak in FFT at 440 Hz
- Demonstrate perfect reconstruction with Fourier series

#### Demo 2: Musical Chord
- Generate multiple frequencies (e.g., C major chord: 261.6, 329.6, 392 Hz)
- Show multiple peaks in spectrum
- Reconstruct using Fourier series

#### Demo 3: Square Wave Decomposition
- Generate square wave
- Show odd harmonics (1, 3, 5, 7, ...)
- Animate series convergence (Gibbs phenomenon)

#### Demo 4: Real-time Audio Analysis
- Capture microphone input
- Display live spectrum
- Show dominant frequencies
- Pitch detection

#### Demo 5: Sensor Data Analysis
- Vibration analysis for mechanical systems
- Identify resonant frequencies
- Detect anomalies in periodic patterns

### Documentation Requirements
- Installation instructions for LuaFFT and LÖVE2D
- API reference for all modules
- Configuration guide for microcontroller integration
- Tutorial examples with expected outputs
- Performance benchmarks for different FFT sizes
- Troubleshooting guide

### Testing Requirements
- Unit tests for FFT accuracy (compare with known transforms)
- Validation against analytical Fourier series
- Performance profiling
- Memory usage monitoring
- Cross-platform testing (Windows, Linux, microcontroller)

## Deliverables
1. Complete working LÖVE2D application
2. Modular, well-documented code
3. Example signals and demo scenarios
4. User guide with screenshots
5. Configuration templates for different microcontrollers

## Current Implementation Status

### Python Development Interfaces

#### shim_interface.py - PC Testing Interface
**Purpose**: Development and testing environment that runs on PC without requiring hardware.

**Key Features**:
- **Dual Mode Operation**: Choose between Python (NumPy/Matplotlib) or Lua execution
- Full visualization with matplotlib plots (Python mode) showing:
  - Time domain waveform
  - Frequency domain spectrum
  - Fourier series reconstruction comparison
  - Harmonic coefficient analysis
- Text-based output for Lua mode (same code as ELM11)
- Signal generation (sine, square, sawtooth, triangle waves)
- FFT analysis with frequency detection
- Fourier series reconstruction and THD calculation
- Real-time simulation with changing frequencies

**Usage**:
```bash
python3 shim_interface.py
```

#### elm11_interface.py - Hardware Control Interface
**Purpose**: PC-side interface for communicating with and controlling the ELM11 microcontroller hardware.

**Key Features**:
- Serial communication with ELM11 microcontroller
- Lua code loading and execution on hardware
- Command-line menu for FFT operations
- Hardware status monitoring
- Real-time data transfer between PC and microcontroller
- Interactive Lua code runner for FFT-focused commands
- Command mode access for advanced ELM11 operations

**Usage**:
```bash
python3 elm11_interface.py
```

**Functions**:
- `load_fft_lua_code()`: Transfers Lua FFT code to ELM11
- `run_fft_analysis()`: Executes FFT analysis commands on hardware
- `get_hardware_status()`: Monitors microcontroller state
- Interactive menu for signal generation, analysis, and visualization

### Current Fourier Folder Structure

The `fourier/` directory contains the Lua implementation that runs on the ELM11 microcontroller:

```
fourier/
├── init.lua               # Core FFT functions, signal generation, and constants
└── fourier_main.lua       # LÖVE2D visualization application (in development)
```

#### init.lua - Core Implementation
**Current Features**:
- Configuration constants (SAMPLE_RATE = 48000, BUFFER_SIZE = 1024, FFT_SIZE = 512)
- Signal generation functions: `generate_sine()`, `generate_square()`, `generate_sawtooth()`, `generate_triangle()`
- Simplified FFT computation (mock implementation for testing)
- Fourier series coefficient extraction: `get_fourier_series()`
- Signal reconstruction from coefficients: `reconstruct_signal()`
- Global state variables for current signal, FFT results, and coefficients

**Expansion Plans**:
- Replace mock FFT with real LuaFFT implementation
- Add window functions (Hamming, Hanning, Blackman)
- Implement inverse FFT capability
- Add power spectral density calculation
- Support variable buffer sizes and zero-padding
- Add coefficient precision and numerical stability improvements

#### fourier_main.lua - LÖVE2D Visualization
**Current Features**:
- LÖVE2D framework setup with window management
- Hardware GPIO and ADC initialization (planned)
- Real-time signal processing framework
- Multiple display modes: time domain, frequency domain, waterfall, Fourier series
- Basic plotting functions for waveforms and spectra
- UI controls and keyboard input handling
- Signal generation functions for testing

**Expansion Plans**:
- Complete hardware sensor integration (ADC, GPIO)
- Implement full visualization components as planned
- Add interactive controls (zoom, pan, scaling)
- Implement waterfall/spectrogram with historical data
- Add phase plot and unwrapped phase display
- Professional visual styling with dark theme
- Real-time performance metrics and FPS display
- Export functionality for data and screenshots

### Development Workflow

1. **Develop in shim_interface.py** (Lua mode) - Test algorithms without hardware
2. **Deploy to ELM11** via elm11_interface.py - Run on actual microcontroller
3. **Unified Codebase** - Same Lua functions work on both PC and hardware
4. **Expand fourier/ modules** - Implement planned features incrementally

This approach ensures algorithms work identically across development and production environments.

## Optional Enhancements
- Real-time filtering (low-pass, high-pass, band-pass)
- Audio output for signal reconstruction
- Save/load session functionality
- Multiple simultaneous plots
- 3D visualization options
- Machine learning integration for pattern recognition
- Network streaming for remote monitoring
