#!/usr/bin/env python3
# ELM11 FFT Testing Interface
# PC-based testing and simulation of FFT analysis
# Can use either Python implementation or Lua code execution

import numpy as np
import matplotlib.pyplot as plt
import questionary
import sys
import subprocess
import os

# FFT Configuration
SAMPLE_RATE = 48000
BUFFER_SIZE = 1024
FFT_SIZE = 512

class FFTAnalyzer:
    def __init__(self, use_lua=False):
        self.use_lua = use_lua
        self.lua_file = 'fourier/fourier_main.lua'
        self.current_signal = np.zeros(BUFFER_SIZE)
        self.fft_result = None
        self.fourier_coeffs = {}
        self.display_mode = "time"
        self.live_mode = False

        if not use_lua:
            self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
            self.fig.suptitle('ELM11 FFT Analyzer - PC Testing Interface')
            plt.tight_layout()

        # Generate initial signal
        self.generate_sine(440, 1.0, 0)
        if not use_lua:
            self.compute_fft()
            self.get_fourier_series(10)
            self.update_plots()

    def check_lua_available(self):
        """Check if Lua interpreter is available"""
        try:
            result = subprocess.run(['lua', '-v'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            try:
                result = subprocess.run(['luajit', '-v'], capture_output=True, text=True)
                return result.returncode == 0
            except FileNotFoundError:
                return False

    def run_lua_code(self, code):
        """Execute Lua code and return result"""
        if not self.check_lua_available():
            print("Lua interpreter not found. Using Python implementation.")
            self.use_lua = False
            return None

        try:
            # Create a temporary Lua script that loads both init and main files
            lua_script = f"""
-- Load initialization
dofile("fourier/init.lua")

-- Load main FFT code
dofile("{self.lua_file}")

-- Execute the requested code
{code}
"""
            with open('/tmp/fft_temp.lua', 'w') as f:
                f.write(lua_script)

            result = subprocess.run(['lua', '/tmp/fft_temp.lua'],
                                  capture_output=True, text=True, timeout=10)
            return result.stdout + result.stderr
        except Exception as e:
            print(f"Error running Lua code: {e}")
            return None

    def generate_sine(self, freq=440, amp=1.0, phase=0):
        """Generate sine wave"""
        if self.use_lua:
            lua_code = f"""
current_signal = generate_sine({freq}, {amp}, {SAMPLE_RATE}, {BUFFER_SIZE})
print("Generated sine wave at " .. {freq} .. " Hz")
"""
            result = self.run_lua_code(lua_code)
            print(result or "Signal generated")
        else:
            t = np.linspace(0, BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE, endpoint=False)
            self.current_signal = amp * np.sin(2 * np.pi * freq * t + phase)
            return self.current_signal

    def generate_square(self, freq=440, amp=1.0):
        """Generate square wave"""
        if self.use_lua:
            lua_code = f"""
current_signal = generate_square({freq}, {amp}, {SAMPLE_RATE}, {BUFFER_SIZE})
print("Generated square wave at " .. {freq} .. " Hz")
"""
            result = self.run_lua_code(lua_code)
            print(result or "Signal generated")
        else:
            t = np.linspace(0, BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE, endpoint=False)
            self.current_signal = amp * np.sign(np.sin(2 * np.pi * freq * t))
            return self.current_signal

    def generate_sawtooth(self, freq=440, amp=1.0):
        """Generate sawtooth wave"""
        if self.use_lua:
            lua_code = f"""
current_signal = generate_sawtooth({freq}, {amp}, {SAMPLE_RATE}, {BUFFER_SIZE})
print("Generated sawtooth wave at " .. {freq} .. " Hz")
"""
            result = self.run_lua_code(lua_code)
            print(result or "Signal generated")
        else:
            t = np.linspace(0, BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE, endpoint=False)
            self.current_signal = amp * (2 * (freq * t - np.floor(freq * t + 0.5)))
            return self.current_signal

    def generate_triangle(self, freq=440, amp=1.0):
        """Generate triangle wave"""
        if self.use_lua:
            lua_code = f"""
current_signal = generate_triangle({freq}, {amp}, {SAMPLE_RATE}, {BUFFER_SIZE})
print("Generated triangle wave at " .. {freq} .. " Hz")
"""
            result = self.run_lua_code(lua_code)
            print(result or "Signal generated")
        else:
            t = np.linspace(0, BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE, endpoint=False)
            self.current_signal = amp * (2 * np.abs(2 * (freq * t - np.floor(freq * t + 0.5))) - 1)
            return self.current_signal

    def compute_fft(self):
        """Compute FFT of current signal"""
        if self.use_lua:
            lua_code = """
fft_result = compute_fft(current_signal)
print("FFT computed")
"""
            result = self.run_lua_code(lua_code)
            print(result or "FFT computed")
        else:
            self.fft_result = np.fft.fft(self.current_signal, n=FFT_SIZE)
            return self.fft_result

    def get_fourier_series(self, n_harmonics=10):
        """Extract Fourier series coefficients"""
        if self.use_lua:
            lua_code = f"""
fourier_coeffs = get_fourier_series(fft_result, {n_harmonics})
print("Fourier series coefficients calculated")
"""
            result = self.run_lua_code(lua_code)
            print(result or "Coefficients calculated")
        else:
            if self.fft_result is None:
                self.compute_fft()

            coeffs = {'a0': 0, 'a_n': [], 'b_n': []}

            # DC component
            coeffs['a0'] = np.real(self.fft_result[0]) / FFT_SIZE * 2

            # Fundamental frequency
            fundamental_idx = 1

            for n in range(1, n_harmonics + 1):
                idx = n * fundamental_idx
                if idx < len(self.fft_result) // 2:
                    real_part = np.real(self.fft_result[idx])
                    imag_part = np.imag(self.fft_result[idx])

                    # Convert to trigonometric form
                    magnitude = np.sqrt(real_part**2 + imag_part**2)
                    phase = np.arctan2(imag_part, real_part)

                    # a_n = 2 * magnitude * cos(phase) / N
                    # b_n = 2 * magnitude * sin(phase) / N
                    coeffs['a_n'].append(2 * magnitude * np.cos(phase) / FFT_SIZE)
                    coeffs['b_n'].append(2 * magnitude * np.sin(phase) / FFT_SIZE)

            self.fourier_coeffs = coeffs
            return coeffs

    def reconstruct_signal(self, n_harmonics=10):
        """Reconstruct signal from Fourier coefficients"""
        if self.use_lua:
            lua_code = f"""
reconstructed = reconstruct_signal({n_harmonics})
print("Signal reconstructed with " .. {n_harmonics} .. " harmonics")
"""
            result = self.run_lua_code(lua_code)
            print(result or "Signal reconstructed")
            return None  # Would need to parse result
        else:
            if not self.fourier_coeffs:
                self.get_fourier_series(n_harmonics)

            t = np.linspace(0, BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE, endpoint=False)
            reconstructed = np.full_like(t, self.fourier_coeffs['a0'] / 2)

            for n in range(len(self.fourier_coeffs['a_n'])):
                freq = (n+1) * 440  # Assuming 440Hz fundamental
                reconstructed += (self.fourier_coeffs['a_n'][n] * np.cos(2 * np.pi * freq * t) +
                                self.fourier_coeffs['b_n'][n] * np.sin(2 * np.pi * freq * t))

            return reconstructed

    def update_plots(self):
        """Update all visualization plots"""
        if self.use_lua:
            print("Plotting not available in Lua mode - use Python implementation for visualization")
            return

        self.axes[0, 0].clear()
        self.axes[0, 1].clear()
        self.axes[1, 0].clear()
        self.axes[1, 1].clear()

        t = np.linspace(0, BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE)

        # Time domain
        self.axes[0, 0].plot(t, self.current_signal, 'g-', linewidth=1)
        self.axes[0, 0].set_title('Time Domain')
        self.axes[0, 0].set_xlabel('Time (s)')
        self.axes[0, 0].set_ylabel('Amplitude')
        self.axes[0, 0].grid(True, alpha=0.3)

        # Frequency domain
        if self.fft_result is not None:
            freqs = np.fft.fftfreq(FFT_SIZE, 1/SAMPLE_RATE)
            magnitudes = np.abs(self.fft_result)[:FFT_SIZE//2]
            freqs = freqs[:FFT_SIZE//2]

            self.axes[0, 1].plot(freqs, 20 * np.log10(magnitudes + 1e-10), 'b-', linewidth=1)
            self.axes[0, 1].set_title('Frequency Domain (dB)')
            self.axes[0, 1].set_xlabel('Frequency (Hz)')
            self.axes[0, 1].set_ylabel('Magnitude (dB)')
            self.axes[0, 1].set_xlim(0, SAMPLE_RATE/2)
            self.axes[0, 1].grid(True, alpha=0.3)

        # Fourier series reconstruction
        if self.fourier_coeffs:
            reconstructed = self.reconstruct_signal()
            self.axes[1, 0].plot(t, self.current_signal, 'g-', alpha=0.7, label='Original')
            self.axes[1, 0].plot(t, reconstructed, 'r-', linewidth=2, label='Reconstructed')
            self.axes[1, 0].set_title('Fourier Series Reconstruction')
            self.axes[1, 0].set_xlabel('Time (s)')
            self.axes[1, 0].set_ylabel('Amplitude')
            self.axes[1, 0].legend()
            self.axes[1, 0].grid(True, alpha=0.3)

        # Fourier coefficients
        if self.fourier_coeffs and self.fourier_coeffs['a_n']:
            harmonics = range(1, len(self.fourier_coeffs['a_n']) + 1)
            a_coeffs = self.fourier_coeffs['a_n']
            b_coeffs = self.fourier_coeffs['b_n']

            self.axes[1, 1].bar(harmonics, a_coeffs, alpha=0.7, label='a_n (cosine)', color='blue')
            self.axes[1, 1].bar(harmonics, b_coeffs, alpha=0.7, label='b_n (sine)', color='red')
            self.axes[1, 1].set_title('Fourier Coefficients')
            self.axes[1, 1].set_xlabel('Harmonic Number')
            self.axes[1, 1].set_ylabel('Coefficient Value')
            self.axes[1, 1].legend()
            self.axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.draw()

def run_signal_generation_demo(analyzer):
    """Demonstrate signal generation"""
    print("Signal Generation Demo")
    print("=" * 40)

    while True:
        choice = questionary.select(
            "Select signal type:",
            choices=[
                "Sine Wave",
                "Square Wave",
                "Sawtooth Wave",
                "Triangle Wave",
                "Custom Parameters",
                "Back to Main Menu"
            ]
        ).ask()

        if choice == "Back to Main Menu":
            break

        if choice == "Sine Wave":
            analyzer.generate_sine(440, 1.0, 0)
        elif choice == "Square Wave":
            analyzer.generate_square(440, 1.0)
        elif choice == "Sawtooth Wave":
            analyzer.generate_sawtooth(440, 1.0)
        elif choice == "Triangle Wave":
            analyzer.generate_triangle(440, 1.0)
        elif choice == "Custom Parameters":
            freq = float(questionary.text("Frequency (Hz):", default="440").ask())
            amp = float(questionary.text("Amplitude:", default="1.0").ask())
            analyzer.generate_sine(freq, amp, 0)

        analyzer.compute_fft()
        analyzer.get_fourier_series(10)
        if not analyzer.use_lua:
            analyzer.update_plots()

        print(f"Generated {choice}")
        if analyzer.use_lua:
            print("Signal generated using Lua code")
        else:
            print("FFT computed and plots updated")
        input("Press Enter to continue...")

def run_fft_analysis_demo(analyzer):
    """Demonstrate FFT analysis"""
    print("FFT Analysis Demo")
    print("=" * 40)

    # Generate a test signal
    analyzer.generate_sine(440, 1.0, 0)
    analyzer.compute_fft()
    analyzer.get_fourier_series(10)
    if not analyzer.use_lua:
        analyzer.update_plots()

    print("FFT Analysis Results:")
    print("-" * 40)

    if analyzer.use_lua:
        print("FFT analysis performed using Lua code")
        print("Results available in Lua environment")
    elif analyzer.fft_result is not None:
        # Find peak frequency
        magnitudes = np.abs(analyzer.fft_result)[:FFT_SIZE//2]
        freqs = np.fft.fftfreq(FFT_SIZE, 1/SAMPLE_RATE)[:FFT_SIZE//2]
        peak_idx = np.argmax(magnitudes)
        peak_freq = freqs[peak_idx]
        peak_mag = magnitudes[peak_idx]

        print(f"Peak frequency: {peak_freq:.1f} Hz")
        print(f"Peak magnitude: {peak_mag:.2f}")
        print(f"Expected: 440 Hz (bin {int(440 * FFT_SIZE / SAMPLE_RATE)})")

        # Show some frequency bins
        print("\nFirst 10 frequency bins:")
        for i in range(min(10, len(magnitudes))):
            print(".1f")

    if not analyzer.use_lua and analyzer.fourier_coeffs:
        print("\nFourier Series Coefficients:")
        print(".3f")
        for i, (a, b) in enumerate(zip(analyzer.fourier_coeffs['a_n'][:5],
                                     analyzer.fourier_coeffs['b_n'][:5])):
            print(".3f")

    input("\nPress Enter to continue...")

def run_fourier_series_demo(analyzer):
    """Demonstrate Fourier series reconstruction"""
    print("Fourier Series Demo")
    print("=" * 40)

    # Test with square wave (rich in harmonics)
    analyzer.generate_square(440, 1.0)
    analyzer.compute_fft()

    if analyzer.use_lua:
        print("Fourier series reconstruction using Lua code")
        print("Reconstructing square wave with harmonics...")
        analyzer.get_fourier_series(10)
        analyzer.reconstruct_signal(10)
        print("Reconstruction completed")
    else:
        print("Reconstructing square wave with increasing harmonics...")
        print("Press Enter to add more harmonics, 'q' to quit")

        max_harmonics = 20
        for n in range(1, max_harmonics + 1, 2):  # Odd harmonics for square wave
            analyzer.get_fourier_series(n)
            analyzer.update_plots()

            print(f"Harmonics: {n} - THD: {calculate_thd(analyzer):.1f}%")
            plt.pause(0.5)  # Brief pause to see animation

            user_input = input(f"Harmonics: {n}. Continue? (Enter/q): ")
            if user_input.lower() == 'q':
                break

def calculate_thd(analyzer):
    """Calculate Total Harmonic Distortion"""
    if not analyzer.fourier_coeffs or not analyzer.fourier_coeffs['a_n']:
        return 0

    fundamental = np.sqrt(analyzer.fourier_coeffs['a_n'][0]**2 +
                         analyzer.fourier_coeffs['b_n'][0]**2)

    harmonics_sum = 0
    for i in range(1, len(analyzer.fourier_coeffs['a_n'])):
        harmonics_sum += analyzer.fourier_coeffs['a_n'][i]**2 + analyzer.fourier_coeffs['b_n'][i]**2

    if fundamental == 0:
        return 0

    thd = np.sqrt(harmonics_sum) / fundamental * 100
    return thd

def run_realtime_simulation(analyzer):
    """Simulate real-time FFT analysis"""
    print("Real-time FFT Simulation")
    print("=" * 40)
    print("Simulating live audio input with changing frequencies")

    analyzer.live_mode = True

    # Simulate changing frequency over time
    freq = 220
    direction = 1

    try:
        for frame in range(100):  # Simulate 100 frames
            # Generate signal with slowly changing frequency
            analyzer.generate_sine(freq, 1.0, 0)
            analyzer.compute_fft()
            analyzer.get_fourier_series(5)

            # Update frequency
            freq += direction * 10
            if freq > 880 or freq < 220:
                direction *= -1

            if not analyzer.use_lua:
                analyzer.update_plots()
                plt.pause(0.1)  # 10 FPS simulation

            print(".1f")

    except KeyboardInterrupt:
        print("\nSimulation stopped")

    analyzer.live_mode = False

def main():
    print("ELM11 FFT Testing Interface")
    print("=" * 40)
    print("PC-based testing and simulation")
    print("No hardware communication required")
    print("")

    # Check if Lua is available and ask user preference
    lua_available = FFTAnalyzer().check_lua_available()
    use_lua = False

    if lua_available:
        choice = questionary.select(
            "Choose implementation:",
            choices=[
                "Python (NumPy/Matplotlib) - Full visualization",
                "Lua (Same code as ELM11) - Text output only"
            ]
        ).ask()

        use_lua = "Lua" in choice
    else:
        print("Lua interpreter not found. Using Python implementation with full visualization.")

    analyzer = FFTAnalyzer(use_lua=use_lua)

    if not use_lua:
        # Generate initial signal and plots for Python mode
        analyzer.generate_sine(440, 1.0, 0)
        analyzer.compute_fft()
        analyzer.get_fourier_series(10)
        analyzer.update_plots()

    while True:
        choice = questionary.select(
            "Choose a demo:",
            choices=[
                "Signal Generation",
                "FFT Analysis",
                "Fourier Series Reconstruction",
                "Real-time Simulation",
                "Show Current Plots",
                "Exit"
            ]
        ).ask()

        if choice == "Signal Generation":
            run_signal_generation_demo(analyzer)
        elif choice == "FFT Analysis":
            run_fft_analysis_demo(analyzer)
        elif choice == "Fourier Series Reconstruction":
            run_fourier_series_demo(analyzer)
        elif choice == "Real-time Simulation":
            run_realtime_simulation(analyzer)
        elif choice == "Show Current Plots":
            if use_lua:
                print("Plotting not available in Lua mode - use Python implementation for visualization")
            else:
                analyzer.update_plots()
                plt.show(block=False)
                input("Press Enter to continue...")
        elif choice == "Exit":
            break

    plt.close('all')
    print("Goodbye!")

if __name__ == "__main__":
    main()
