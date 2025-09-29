# Lua FFT Analyzer & Visualizer

**Real-time Fourier analysis and visualization toolkit for Lua microcontrollers with LÖVE2D**

## 🌊 Overview

A comprehensive FFT analysis system combining LuaFFT/FFTW3 processing with beautiful real-time visualizations. Designed for embedded systems, sensor analysis, and educational demonstrations of Fourier theory.

## ✨ Features

- **Dual FFT Engine**: Pure Lua (LuaFFT) or high-performance (FFTW3) implementations
- **Fourier Series Analysis**: Extract and visualize trigonometric coefficients (a₀, aₙ, bₙ)
- **Real-time Visualization**: 
  - Time-domain waveforms
  - Frequency spectrum (FFT)
  - Waterfall/spectrogram display
  - Interactive Fourier series reconstruction
- **Signal Generation**: Sine, square, sawtooth, triangle, and custom waveforms
- **Microcontroller Ready**: Optimized for resource-constrained environments
- **Educational Tools**: Demonstrate Gibbs phenomenon, harmonic analysis, and signal decomposition

## 🎯 Use Cases

- Audio spectrum analysis
- Vibration monitoring
- Sensor data processing
- Signal processing education
- Real-time frequency detection
- Harmonic analysis of periodic signals

## 🚀 Quick Start

```lua
local fft = require("fft")
local signal = require("signal.generator")

-- Generate test signal
local wave = signal.sine(440, 1.0, 48000, 1024)

-- Perform FFT and extract Fourier coefficients
local spectrum = fft.analyze(wave)
local coefficients = fft.get_fourier_series(spectrum, 10) -- First 10 harmonics

-- Visualize with LÖVE2D
love.graphics.draw(spectrum.plot)
```

## 🔧 Interface Files

### `elm11_interface.py` - Hardware Control Interface
**Purpose**: PC-side interface for communicating with and controlling the ELM11 microcontroller hardware.

**Key Features**:
- Serial communication with ELM11 microcontroller
- Lua code loading and execution on hardware
- Command-line menu for FFT operations
- Hardware status monitoring
- Real-time data transfer between PC and microcontroller

**Usage**:
```bash
python3 elm11_interface.py
```

**Functions**:
- `load_fft_lua_code()`: Transfers Lua FFT code to ELM11
- `run_fft_analysis()`: Executes FFT analysis commands on hardware
- `get_hardware_status()`: Monitors microcontroller state
- Interactive menu for signal generation, analysis, and visualization

### `shim_interface.py` - PC Testing Interface
**Purpose**: Development and testing environment that runs on PC without requiring hardware.

**Key Features**:
- **Dual Mode Operation**: Choose between Python (NumPy/Matplotlib) or Lua execution
- Full visualization with matplotlib plots (Python mode)
- Text-based output for Lua mode (same code as ELM11)
- Signal generation and FFT analysis
- Fourier series reconstruction and THD calculation
- Real-time simulation capabilities

**Usage**:
```bash
python3 shim_interface.py
```

**Modes**:
- **Python Mode**: Full GUI with 4-panel visualization (time domain, frequency domain, Fourier reconstruction, coefficient analysis)
- **Lua Mode**: Text output using identical Lua code as ELM11 hardware - perfect for unified testing

**Demo Options**:
- Signal Generation (sine, square, sawtooth, triangle waves)
- FFT Analysis with frequency detection
- Fourier Series Reconstruction with harmonic visualization
- Real-time Simulation with changing frequencies

## 📁 Project Structure

```
ELM11-Lua-FFT/
├── elm11_interface.py      # Hardware control interface
├── shim_interface.py       # PC testing interface
├── fourier/
│   ├── init.lua           # Core FFT functions and constants
│   └── fourier_main.lua   # LÖVE2D visualization for ELM11
├── docs/
│   ├── ELM11_Datasheet.*  # Hardware documentation
│   └── README.md
└── README.md
```

## 🔄 Development Workflow

1. **Develop in shim_interface.py** (Lua mode) - Test algorithms without hardware
2. **Deploy to ELM11** via elm11_interface.py - Run on actual microcontroller
3. **Unified Codebase** - Same Lua functions work on both PC and hardware

This approach ensures your FFT algorithms work identically across development and production environments.
