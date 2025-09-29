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
