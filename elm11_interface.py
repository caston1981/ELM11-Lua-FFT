#!/usr/bin/env python3
# ELM11 FFT Interface
# Python script for PC-side communication with ELM11 microcontroller
# Handles serial communication and Lua code management for FFT operations

import serial
import time
import sys
import glob
import questionary
import os

# Serial configuration
SERIAL_PORTS = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
if not SERIAL_PORTS:
    SERIAL_PORTS = ['/dev/ttyUSB0']  # fallback
BAUD_RATES = [115200, 9600, 19200, 38400, 57600]
TIMEOUT = 2

def connect_serial():
    """Connect to ELM11 serial port"""
    for port in SERIAL_PORTS:
        for baud in BAUD_RATES:
            try:
                ser = serial.Serial(port, baud, timeout=TIMEOUT)
                print(f"Connected to {port} at {baud} baud")
                # Wait for ELM11 to be ready
                time.sleep(2)
                # Clear any pending data
                ser.read(1024)
                # Ensure we're in REPL mode (exit command mode if in it)
                ser.write(b'q\r\n')  # Exit any listing mode
                ser.flush()
                time.sleep(0.5)
                ser.read(256)  # Clear response
                ser.write(b'exit\r\n')
                ser.flush()
                time.sleep(0.5)
                ser.read(256)  # Clear response
                ser.write(b'exit\r\n')  # Send again just in case
                ser.flush()
                time.sleep(0.5)
                ser.read(256)  # Clear response
                # Send newline to get prompt
                ser.write(b'\r\n')
                ser.flush()
                time.sleep(0.5)
                ser.read(256)  # Clear prompt
                return ser
            except Exception as e:
                continue
    print("Failed to connect to ELM11")
    return None

def send_lua_code(ser, code):
    """Send Lua code to ELM11 and return response"""
    try:
        # Send code in chunks if it's very large
        chunk_size = 1024
        if len(code) > chunk_size:
            # Send in chunks with small delays
            for i in range(0, len(code), chunk_size):
                chunk = code[i:i+chunk_size]
                ser.write(chunk.encode())
                ser.flush()
                time.sleep(0.1)  # Small delay between chunks
            ser.write(b'\r\n')  # Final newline
            ser.flush()
        else:
            ser.write((code + '\r\n').encode())
            ser.flush()

        # Wait longer for large code blocks
        wait_time = min(2.0, 0.5 + len(code) / 2000)  # Scale wait time with code size
        time.sleep(wait_time)

        # Read response (may be multiple chunks)
        response = b""
        for _ in range(5):  # Try reading multiple times
            chunk = ser.read(1024)
            if not chunk:
                break
            response += chunk
            time.sleep(0.1)

        return response.decode(errors='replace')
    except Exception as e:
        return f"Error: {e}"

def load_fft_lua_code(ser):
    """Load the FFT Lua code onto ELM11"""
    print("Loading FFT Lua code onto ELM11...")
    try:
        with open('fourier/fourier_main.lua', 'r') as f:
            lua_code = f.read()
    except FileNotFoundError:
        print("Error: fourier/fourier_main.lua not found")
        return False

    print("Sending FFT code to ELM11...")
    response = send_lua_code(ser, lua_code)
    if "Error" in response:
        print("Failed to load FFT code:")
        print(response)
        return False

    print("FFT code loaded successfully!")
    print("ELM11 is now running FFT analysis.")
    return True

def run_fft_analysis(ser):
    """Run FFT analysis on ELM11"""
    print("FFT Analysis on ELM11")
    print("=" * 40)
    print("Running FFT analysis on the microcontroller...")

    if not questionary.confirm("Ready to run FFT analysis on ELM11?").ask():
        return

    # First load the FFT code if not already loaded
    if not load_fft_lua_code(ser):
        return

    # Run the analysis
    analysis_code = "run_fft_analysis()"
    print("Starting FFT analysis...")
    response = send_lua_code(ser, analysis_code)
    print("Analysis response:")
    print(response)

    print("")
    input("Press Enter to return to main menu...")

def run_signal_generation(ser):
    """Generate test signals on ELM11"""
    print("Signal Generation on ELM11")
    print("=" * 40)

    signal_types = {
        "Sine Wave": "generate_sine(440, 1.0, 48000, 1024)",
        "Square Wave": "generate_square(440, 1.0, 48000, 1024)",
        "Sawtooth Wave": "generate_sawtooth(440, 1.0, 48000, 1024)",
        "Triangle Wave": "generate_triangle(440, 1.0, 48000, 1024)",
        "Custom Waveform": "generate_custom()"
    }

    choice = questionary.select(
        "Select signal type to generate on ELM11:",
        choices=list(signal_types.keys()) + ["Back"]
    ).ask()

    if choice == "Back":
        return

    code = signal_types[choice]
    print(f"Generating {choice} on ELM11...")
    response = send_lua_code(ser, code)
    print("Generation response:")
    print(response)
    print("")
    input("Press Enter to continue...")

def run_fourier_series_demo(ser):
    """Run Fourier series demonstration on ELM11"""
    print("Fourier Series Demo on ELM11")
    print("=" * 40)
    print("This will demonstrate Fourier series reconstruction on the microcontroller.")

    if not questionary.confirm("Ready to run Fourier series demo on ELM11?").ask():
        return

    # Load the demo code
    if not load_fft_lua_code(ser):
        return

    # Run the demo
    demo_code = "run_fourier_demo()"
    print("Starting Fourier series demonstration...")
    response = send_lua_code(ser, demo_code)
    print("Demo response:")
    print(response)

    print("")
    input("Press Enter to return to main menu...")

def run_real_time_fft(ser):
    """Run real-time FFT visualization on ELM11"""
    print("Real-time FFT on ELM11")
    print("=" * 40)
    print("This will display real-time FFT analysis of sensor data on ELM11.")
    print("Requires microphone or vibration sensor connected to ELM11.")

    if not questionary.confirm("Ready for real-time FFT on ELM11?").ask():
        return

    # Load the real-time FFT code
    if not load_fft_lua_code(ser):
        return

    print("Real-time FFT is now running on ELM11.")
    print("Check the ELM11 display for live frequency analysis.")
    print("")

    input("Press Enter to return to main menu... (FFT continues running on ELM11)")

def run_lua_interactive(ser):
    """Interactive Lua code runner on ELM11 - FFT focused"""
    examples = {
        "Load FFT Library": 'require("fft")',
        "Generate Sine Wave": 'local signal = {}; for i=1,1024 do signal[i] = math.sin(2*math.pi*440*i/48000) end',
        "Compute FFT": 'local spectrum = fft.analyze(signal)',
        "Extract Magnitudes": 'local mag = {}; for i=1,#spectrum/2 do mag[i] = math.sqrt(spectrum[i*2-1]^2 + spectrum[i*2]^2) end',
        "Find Peak Frequency": 'local peak_idx = 1; for i=2,#mag do if mag[i] > mag[peak_idx] then peak_idx = i end end; print("Peak at bin:", peak_idx)',
        "Fourier Series Coefficients": 'local coeffs = fft.get_fourier_series(spectrum, 5)',
        "ELM11 GPIO for Sensors": 'pin_mode(PIN1, GPIO_IN); local sensor_val = analog_read(PIN1)',
        "Time-domain Plot": 'plot_signal(signal, "Time Domain")'
    }

    while True:
        choice = questionary.select(
            "Lua Code Runner on ELM11 (FFT Focus):",
            choices=[
                "Enter Custom Code",
                "Choose FFT Example",
                "Back to Main Menu"
            ]
        ).ask()

        if choice == "Enter Custom Code":
            code = questionary.text("Enter Lua code to run on ELM11:").ask()
            if code and code.strip():
                print("Sending to ELM11...")
                response = send_lua_code(ser, code)
                print("Response from ELM11:")
                print(response)
                print("-" * 40)
        elif choice == "Choose FFT Example":
            example_choice = questionary.select(
                "Select an FFT example to run on ELM11:",
                choices=list(examples.keys()) + ["Back"]
            ).ask()
            if example_choice != "Back":
                code = examples[example_choice]
                print(f"Example code: {code}")
                confirm = questionary.confirm("Send this code to ELM11?").ask()
                if confirm:
                    print("Sending to ELM11...")
                    response = send_lua_code(ser, code)
                    print("Response from ELM11:")
                    print(response)
                    print("-" * 40)
        elif choice == "Back to Main Menu":
            break

def enter_command_mode(ser):
    """Enter Command Mode on ELM11"""
    print("Entering Command Mode on ELM11...")
    ser.write(b'command\r\n')
    ser.flush()
    time.sleep(0.5)
    response = ser.read(512)
    print("Command Mode response:")
    print(response.decode(errors='replace'))

    while True:
        choice = questionary.select(
            "Command Mode on ELM11:",
            choices=[
                "List Commands",
                "Show Help",
                "Send Custom Command",
                "Exit to REPL"
            ]
        ).ask()

        if choice == "List Commands":
            ser.write(b'list|commands\r\n')
            ser.flush()
            time.sleep(1)
            response = ser.read(2048)
            print("Commands list:")
            print(response.decode(errors='replace'))
        elif choice == "Show Help":
            ser.write(b'list|help\r\n')
            ser.flush()
            time.sleep(1)
            response = ser.read(4096)  # Help is long
            print("Help:")
            print(response.decode(errors='replace'))
        elif choice == "Send Custom Command":
            cmd = questionary.text("Enter command (e.g., 'list|programs'):").ask()
            if cmd.strip():
                ser.write((cmd + '\r\n').encode())
                ser.flush()
                time.sleep(1)
                response = ser.read(2048)
                print("Response:")
                print(response.decode(errors='replace'))
        elif choice == "Exit to REPL":
            ser.write(b'exit\r\n')
            ser.flush()
            time.sleep(0.5)
            response = ser.read(256)
            print("Exited to REPL")
            break

def show_boot_log(ser):
    """Show ELM11 boot log"""
    print("To show the boot log, the ELM11 needs to be reset.")
    print("This will disconnect the serial connection.")
    confirm = questionary.confirm("Proceed with reset? (You may need to restart the interface afterward)").ask()
    if confirm:
        # Try to send a reset command if available
        ser.write(b'reset\r\n')  # Assuming there's a reset command
        ser.flush()
        time.sleep(1)
        ser.close()
        print("Device reset. Please unplug/replug or press RST button to see boot log.")
        print("Restart the interface after the device reboots.")
        return True  # Indicate we closed the connection
    return False

def main():
    print("ELM11 FFT Interface")
    print("=" * 40)
    print("PC-side interface for FFT operations on ELM11 microcontroller")
    print("Communicates with ELM11 and manages Lua FFT code")
    print("")

    ser = connect_serial()
    if not ser:
        print("\nNo ELM11 hardware detected.")
        print("Please connect ELM11 and try again.")
        return

    while True:
        choice = questionary.select(
            "Choose an option:",
            choices=[
                "Run FFT Analysis",
                "Signal Generation",
                "Fourier Series Demo",
                "Real-time FFT",
                "Interactive Lua (FFT)",
                "Enter Command Mode",
                "Show Boot Log",
                "Load FFT Code",
                "Exit"
            ]
        ).ask()

        if choice == "Run FFT Analysis":
            run_fft_analysis(ser)
        elif choice == "Signal Generation":
            run_signal_generation(ser)
        elif choice == "Fourier Series Demo":
            run_fourier_series_demo(ser)
        elif choice == "Real-time FFT":
            run_real_time_fft(ser)
        elif choice == "Interactive Lua (FFT)":
            run_lua_interactive(ser)
        elif choice == "Enter Command Mode":
            enter_command_mode(ser)
        elif choice == "Show Boot Log":
            if show_boot_log(ser):
                break  # Connection closed, exit loop
        elif choice == "Load FFT Code":
            load_fft_lua_code(ser)
        elif choice == "Exit":
            break

    ser.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()
