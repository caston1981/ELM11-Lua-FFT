#!/usr/bin/env python3
# ELM11 Interactive Interface
# Provides a menu-driven interface to interact with ELM11 via serial
# Allows running Lua code and has a placeholder for Citrus Doom

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

def run_lua_interactive(ser):
    """Interactive Lua code runner"""
    examples = {
        "Print Hello World": 'print("Hello, World!")',
        "Simple Math": 'print(2 + 3 * 4)',
        "Variable Assignment": 'x = 42; print("x =", x)',
        "Loop Example": 'for i = 1, 5 do print("Count:", i) end',
        "Function Example": 'function greet(name) return "Hello, " .. name end; print(greet("ELM11"))',
        "Table Example": 't = {a=1, b=2}; print(t.a, t.b)',
        "ELM11 Specific - GPIO": 'print("GPIO functions: pin_mode, digital_write, etc.")',
        "ELM11 Specific - Time": 'print("Current time:", os.time())'
    }

    while True:
        choice = questionary.select(
            "Lua Code Runner:",
            choices=[
                "Enter Custom Code",
                "Choose Example",
                "Back to Main Menu"
            ]
        ).ask()

        if choice == "Enter Custom Code":
            code = questionary.text("Enter Lua code:").ask()
            if code and code.strip():
                print("Sending to ELM11...")
                response = send_lua_code(ser, code)
                print("Response:")
                print(response)
                print("-" * 40)
        elif choice == "Choose Example":
            example_choice = questionary.select(
                "Select an example:",
                choices=list(examples.keys()) + ["Back"]
            ).ask()
            if example_choice != "Back":
                code = examples[example_choice]
                print(f"Example code: {code}")
                confirm = questionary.confirm("Send this code to ELM11?").ask()
                if confirm:
                    print("Sending to ELM11...")
                    response = send_lua_code(ser, code)
                    print("Response:")
                    print(response)
                    print("-" * 40)
        elif choice == "Back to Main Menu":
            break

def enter_command_mode(ser):
    """Enter Command Mode and provide interactive interface"""
    print("Entering Command Mode...")
    ser.write(b'command\r\n')
    ser.flush()
    time.sleep(0.5)
    response = ser.read(512)
    print("Command Mode response:")
    print(response.decode(errors='replace'))
    
    while True:
        choice = questionary.select(
            "Command Mode:",
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
            # Note: This might require scrolling, but we'll capture what we can
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
    """Attempt to show boot log by resetting device"""
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

def run_gpio_test(ser):
    """Run GPIO button testing functionality"""
    print("GPIO Button Test")
    print("=" * 40)
    print("This will test GPIO buttons connected to pins 1-5 on your ELM11.")
    print("Make sure you have buttons connected to GPIO pins:")
    print("  Pin 1: UP button")
    print("  Pin 2: DOWN button")
    print("  Pin 3: LEFT button")
    print("  Pin 4: RIGHT button")
    print("  Pin 5: SHOOT button")
    print("")

    if not questionary.confirm("Do you have buttons connected and ready to test?").ask():
        return

    # Load the GPIO test script
    try:
        with open('gpio_test_repl.lua', 'r') as f:
            test_code = f.read()
    except FileNotFoundError:
        print("Error: gpio_test_repl.lua not found in current directory")
        return

    print("Loading GPIO test script...")
    response = send_lua_code(ser, test_code)
    if "Error" in response:
        print("Failed to load test script:")
        print(response)
        return

    print("GPIO test script loaded successfully!")
    print("The test will show button states in real-time.")
    print("Press buttons to see them register as PRESSED.")
    print("")

    # Run the test
    test_code = "test_input(false)"
    print("Starting GPIO button test...")
    response = send_lua_code(ser, test_code)
    print("Test response:")
    print(response)

    print("")
    print("Test complete! You can also run individual button checks:")
    print("  getButtonUp(), getButtonDown(), getButtonLeft(), getButtonRight(), getButtonShoot()")
    print("")
    input("Press Enter to return to main menu...")

def run_gpio_led_test(ser):
    """Run GPIO LED testing functionality"""
    print("GPIO LED Test")
    print("=" * 40)
    print("This will test GPIO output pins 0-15 by lighting LEDs sequentially.")
    print("Make sure you have LEDs and resistors connected to GPIO pins:")
    print("  Each GPIO pin (0-15) -> LED anode -> 330Ω resistor -> GND")
    print("See GPIO_Test_Wiring.md for detailed wiring instructions.")
    print("")

    if not questionary.confirm("Do you have LEDs wired to GPIO pins 0-15 and ready to test?").ask():
        return

    # Load the GPIO LED test script
    try:
        with open('gpio_led_test.lua', 'r') as f:
            test_code = f.read()
    except FileNotFoundError:
        print("Error: gpio_led_test.lua not found in current directory")
        return

    print("Loading GPIO LED test script...")
    response = send_lua_code(ser, test_code)
    if "Error" in response:
        print("Failed to load test script:")
        print(response)
        return

    print("GPIO LED test script loaded successfully!")
    print("LEDs should light up sequentially (GPIO0 to GPIO15, 1 second each).")
    print("Press Ctrl+C in the serial terminal to stop the test.")
    print("")
    print("Starting GPIO LED test... (script runs continuously)")
    print("Check your LEDs - they should cycle through all pins.")
    print("")
    input("Press Enter to return to main menu... (test continues running on ELM11)")

def run_lcd_test(ser):
    """Run LCD display testing functionality"""
    print("LCD Display Test")
    print("=" * 40)
    print("This will test your ST7735S 1.44\" 128x128 TFT LCD display.")
    print("Make sure your LCD is properly wired:")
    print("  - SPI_CS -> ELM11 SPI_CS pin")
    print("  - SPI_CLK -> ELM11 SPI_CLK pin")
    print("  - SPI_MOSI -> ELM11 SPI_MOSI pin")
    print("  - DC -> ELM11 GPIO pin")
    print("  - RST -> ELM11 GPIO pin")
    print("  - VCC -> 3.3V")
    print("  - GND -> GND")
    print("")

    if not questionary.confirm("Is your ST7735S LCD connected and ready to test?").ask():
        return

    # Load the LCD test script
    try:
        with open('st7735_test.lua', 'r') as f:
            test_code = f.read()
    except FileNotFoundError:
        print("Error: st7735_test.lua not found in current directory")
        return

    print("Loading ST7735S test script...")
    response = send_lua_code(ser, test_code)
    if "Error" in response:
        print("Failed to load test script:")
        print(response)
        return

    print("ST7735S test script loaded successfully!")
    print("The test will display colors, shapes, and animations on your LCD.")
    print("This may take a minute to complete...")
    print("")

    # The test script runs automatically when loaded
    print("Test completed! Check your LCD display.")
    print("You should have seen:")
    print("  - Screen clear")
    print("  - Colored rectangles (red, green, blue, yellow)")
    print("  - White cross lines")
    print("  - Additional shapes and text")
    print("  - Simple animation")
    print("")
    print("If you didn't see these, check your wiring and try again.")
    print("")
    input("Press Enter to return to main menu...")

def run_games_menu(ser):
    """Menu for selecting different games to run"""
    while True:
        game_choice = questionary.select(
            "Select a game to run:",
            choices=[
                "Citrus Doom",
                "Pong",
                "Snake",
                "Pac-Man", 
                "Space Invaders",
                "Back to Main Menu"
            ]
        ).ask()

        if game_choice == "Citrus Doom":
            print("Citrus Doom - A Doom port for ELM11")
            print("This would load the full Doom engine and level data")
            print("Status: Not implemented yet.")
        elif game_choice == "Pong":
            print("Pong - Classic paddle ball game")
            print("Player vs AI paddle with scoring system")
            print("Status: Code written (games/pong/pong.lua)")
            print("To run: Upload games/pong/pong.lua to ELM11 and execute")
            print("Controls: Use Up/Down inputs to move paddle, Start to begin")
        elif game_choice == "Snake":
            print("Snake - Guide the snake to eat food and grow")
            print("Classic arcade game with increasing difficulty")
            print("Status: Code written (games/snake/snake.lua)")
            print("To run: Upload games/snake/snake.lua to ELM11 and execute")
            print("Controls: Use Up/Down/Left/Right inputs, Start to begin/restart")
        elif game_choice == "Pac-Man":
            print("Pac-Man - Navigate mazes eating dots while avoiding ghosts")
            print("Collect power pellets to turn the tables on ghosts")
            print("Status: Code written (games/pacman/pacman.lua)")
            print("To run: Upload games/pacman/pacman.lua to ELM11 and execute")
            print("Controls: Up/Down/Left/Right to move Pac-Man")
        elif game_choice == "Space Invaders":
            print("Space Invaders - Defend Earth from alien invaders")
            print("Shoot aliens while avoiding their fire")
            print("Status: Code written (games/space_invaders/space_invaders.lua)")
            print("To run: Upload games/space_invaders/space_invaders.lua to ELM11 and execute")
            print("Controls: Left/Right to move, Shoot to fire")
        elif game_choice == "Back to Main Menu":
            break
        
        input("Press Enter to continue...")

def run_love2d_examples(ser):
    """Menu for selecting Love2D-style examples adapted for ELM11"""
    while True:
        example_choice = questionary.select(
            "Select a Love2D Example (adapted for ELM11):",
            choices=[
                "Hello World",
                "Shapes",
                "Animation",
                "Input Demo",
                "Particles",
                "Back to Main Menu"
            ]
        ).ask()

        if example_choice == "Back to Main Menu":
            break

        # Map menu choices to file names
        file_map = {
            "Hello World": "hello_world.lua",
            "Shapes": "shapes.lua",
            "Animation": "animation.lua",
            "Input Demo": "input_demo.lua",
            "Particles": "particles.lua"
        }

        filename = file_map.get(example_choice)
        if filename:
            filepath = f"love2d_examples/{filename}"
            try:
                with open(filepath, 'r') as f:
                    lua_code = f.read()

                print(f"\nLoading {example_choice} example...")
                print(f"Running {filepath} on ELM11...")

                # Send the Lua code to ELM11
                response = send_lua_code(ser, lua_code)

                print(f"\n{example_choice} example loaded successfully!")
                print("The example should now be running on your ELM11 device.")

            except FileNotFoundError:
                print(f"Error: {filepath} not found. Please ensure the example files exist.")
            except Exception as e:
                print(f"Error loading example: {e}")

        input("\nPress Enter to continue...")

def run_love2d_games(ser):
    """Menu for selecting Love2D games adapted for ELM11"""
    while True:
        game_choice = questionary.select(
            "Select a Love2D Game (adapted for ELM11):",
            choices=[
                "LovePong - Pong Clone",
                "LoveBirb - Flappy Bird Clone",
                "LovePlatform - Platformer Prototype",
                "Love2D Snake - Snake Game",
                "Love2D Pac-Man - Pac-Man Game",
                "Love2D Space Invaders - Space Invaders Game",
                "Back to Main Menu"
            ]
        ).ask()

        if game_choice == "Back to Main Menu":
            break

        # Map menu choices to file names
        file_map = {
            "LovePong - Pong Clone": "love_pong.lua",
            "LoveBirb - Flappy Bird Clone": "love_birb.lua",
            "LovePlatform - Platformer Prototype": "love_platform.lua",
            "Love2D Snake - Snake Game": "love2d_snake.lua",
            "Love2D Pac-Man - Pac-Man Game": "love2d_pacman.lua",
            "Love2D Space Invaders - Space Invaders Game": "love2d_space_invaders.lua"
        }

        filename = file_map.get(game_choice.split(" - ")[0])
        if filename:
            filepath = f"love2d_games/{filename}"
            try:
                with open(filepath, 'r') as f:
                    lua_code = f.read()

                print(f"\nLoading {game_choice}...")
                print(f"Running {filepath} on ELM11...")

                # Send the Lua code to ELM11
                response = send_lua_code(ser, lua_code)

                print(f"\n{game_choice} loaded successfully!")
                print("The game should now be running on your ELM11 device.")

            except FileNotFoundError:
                print(f"Error: {filepath} not found. Please ensure the game files exist.")
            except Exception as e:
                print(f"Error loading game: {e}")

        input("\nPress Enter to continue...")

def run_simulation_mode():
    """Run games in simulation mode without ELM11 hardware"""
    print("\nSimulation Mode")
    print("=" * 40)
    print("This mode simulates the ELM11 display and input system.")
    print("Games will run in a graphical window on your computer.")
    print("Note: This is a basic simulation - actual ELM11 performance may differ.\n")

    while True:
        choice = questionary.select(
            "Simulation Mode:",
            choices=[
                "Love2D Examples",
                "Love2D Games",
                "Classic Games",
                "Back to Main Menu"
            ]
        ).ask()

        if choice == "Love2D Examples":
            run_simulated_love2d_examples()
        elif choice == "Love2D Games":
            run_simulated_love2d_games()
        elif choice == "Classic Games":
            run_simulated_classic_games()
        elif choice == "Back to Main Menu":
            break

def run_simulated_love2d_examples():
    """Run Love2D examples in simulation mode"""
    while True:
        example_choice = questionary.select(
            "Select a Love2D Example to simulate:",
            choices=[
                "Hello World - Basic text display",
                "Shapes - Drawing geometric shapes",
                "Animation - Moving objects and time-based updates",
                "Input Demo - Button input detection",
                "Particles - Particle system effects",
                "Back to Simulation Menu"
            ]
        ).ask()

        if example_choice == "Back to Simulation Menu":
            break

        # Map choices to files
        file_map = {
            "Hello World - Basic text display": "love2d_examples/hello_world.lua",
            "Shapes - Drawing geometric shapes": "love2d_examples/shapes.lua",
            "Animation - Moving objects and time-based updates": "love2d_examples/animation.lua",
            "Input Demo - Button input detection": "love2d_examples/input_demo.lua",
            "Particles - Particle system effects": "love2d_examples/particles.lua"
        }

        filepath = file_map.get(example_choice)
        if filepath:
            print(f"\nSimulating {example_choice}...")
            print("Note: This is a text-based simulation. For full graphics, connect ELM11 hardware.")
            print("The actual game would display graphics on the ELM11 screen.")

            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                # Show key parts of the code
                print(f"\n--- Code from {filepath} ---")
                lines = content.split('\n')
                for i, line in enumerate(lines[:20]):  # Show first 20 lines
                    print("2d")
                if len(lines) > 20:
                    print(f"... ({len(lines)-20} more lines)")

                print("\n--- Simulation Notes ---")
                print("• love.load() → Game initialization")
                print("• love.update(dt) → Game logic (60 FPS target)")
                print("• love.draw() → Screen rendering")
                print("• property.getBool() → Input detection")
                print("• screen.drawText()/drawRect() → Display output")

            except FileNotFoundError:
                print(f"Error: {filepath} not found.")
            except Exception as e:
                print(f"Error: {e}")

        input("\nPress Enter to continue...")

def run_simulated_love2d_games():
    """Run Love2D games in simulation mode"""
    while True:
        game_choice = questionary.select(
            "Select a Love2D Game to simulate:",
            choices=[
                "LovePong - Pong with physics",
                "LoveBirb - Flappy Bird clone",
                "LovePlatform - Platformer prototype",
                "Love2D Snake - Classic Snake game",
                "Love2D Pac-Man - Pac-Man with ghosts",
                "Love2D Space Invaders - Alien shooter",
                "Back to Simulation Menu"
            ]
        ).ask()

        if game_choice == "Back to Simulation Menu":
            break

        # Map choices to files
        file_map = {
            "LovePong - Pong with physics": "love2d_games/love_pong.lua",
            "LoveBirb - Flappy Bird clone": "love2d_games/love_birb.lua",
            "LovePlatform - Platformer prototype": "love2d_games/love_platform.lua",
            "Love2D Snake - Classic Snake game": "love2d_games/love2d_snake.lua",
            "Love2D Pac-Man - Pac-Man with ghosts": "love2d_games/love2d_pacman.lua",
            "Love2D Space Invaders - Alien shooter": "love2d_games/love2d_space_invaders.lua"
        }

        filepath = file_map.get(game_choice.split(" - ")[0])
        if filepath:
            print(f"\nSimulating {game_choice}...")
            print("Note: This is a text-based simulation. For full gameplay, connect ELM11 hardware.")
            print("The actual game would be fully playable on the ELM11 device.")

            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                # Extract game info
                lines = content.split('\n')
                game_title = ""
                controls = []
                features = []

                for line in lines[:50]:  # Check first 50 lines for comments
                    line = line.strip()
                    if line.startswith("--") and "Game" in line:
                        game_title = line[2:].strip()
                    elif line.startswith("--") and ("Controls:" in line or "controls:" in line.lower()):
                        controls.append(line[2:].strip())
                    elif line.startswith("--") and ("Features:" in line or "features:" in line.lower()):
                        features.append(line[2:].strip())

                print(f"\n--- {game_title} ---")
                if features:
                    print("Features:")
                    for feature in features[:5]:  # Show up to 5 features
                        print(f"• {feature}")

                print("\nControls (when running on ELM11):")
                print("• Arrow Keys: Movement (Up/Down/Left/Right)")
                print("• A Button: Primary action (jump/shoot/flap)")
                print("• B Button: Secondary action")
                print("• Start Button: Begin game/restart")

                print("\nGame Structure:")
                print("• State management (menu/playing/game over)")
                print("• Entity system (player, enemies, projectiles)")
                print("• Collision detection and physics")
                print("• Scoring and progression systems")

                # Show code sample
                print(f"\n--- Sample Code from {filepath} ---")
                # Find love.load function
                in_load = False
                load_lines = []
                for line in lines:
                    if line.strip().startswith("function love.load()"):
                        in_load = True
                    elif in_load and line.strip().startswith("end"):
                        load_lines.append(line)
                        break
                    elif in_load:
                        load_lines.append(line)

                if load_lines:
                    print("love.load() function:")
                    for line in load_lines[:10]:
                        print("2d")
                    if len(load_lines) > 10:
                        print("    ...")

            except FileNotFoundError:
                print(f"Error: {filepath} not found.")
            except Exception as e:
                print(f"Error: {e}")

        input("\nPress Enter to continue...")

def run_simulated_classic_games():
    """Run classic games in simulation mode"""
    while True:
        game_choice = questionary.select(
            "Select a Classic Game to simulate:",
            choices=[
                "Snake - Grid-based snake game",
                "Pong - Classic paddle ball game",
                "Space Invaders - Alien shooter",
                "Pac-Man - Maze navigation game",
                "Back to Simulation Menu"
            ]
        ).ask()

        if game_choice == "Back to Simulation Menu":
            break

        # Map choices to files
        file_map = {
            "Snake - Grid-based snake game": "games/snake/snake.lua",
            "Pong - Classic paddle ball game": "games/pong/pong.lua",
            "Space Invaders - Alien shooter": "games/space_invaders/space_invaders.lua",
            "Pac-Man - Maze navigation game": "games/pacman/pacman.lua"
        }

        filepath = file_map.get(game_choice.split(" - ")[0])
        if filepath:
            print(f"\nSimulating {game_choice}...")
            print("Note: This is a text-based simulation. For full gameplay, connect ELM11 hardware.")

            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                print(f"\n--- Code from {filepath} ---")
                lines = content.split('\n')
                for i, line in enumerate(lines[:15]):  # Show first 15 lines
                    print("2d")
                if len(lines) > 15:
                    print(f"... ({len(lines)-15} more lines)")

                print("\n--- Simulation Notes ---")
                print("• Direct ELM11 API usage (screen.drawRect, property.getBool)")
                print("• Game loop with onTick() and onDraw() functions")
                print("• Optimized for 66MHz processor and 288x160 display")

            except FileNotFoundError:
                print(f"Error: {filepath} not found.")
            except Exception as e:
                print(f"Error: {e}")

        input("\nPress Enter to continue...")

def main():
    print("ELM11 Interactive Interface")
    print("=" * 40)

    # Check if we should run in simulation mode (no hardware required)
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        run_simulation_mode()
        return

    ser = connect_serial()
    if not ser:
        print("\nNo ELM11 hardware detected.")
        print("Would you like to run in simulation mode instead?")
        if questionary.confirm("Run in simulation mode?").ask():
            run_simulation_mode()
        return

    while True:
        choice = questionary.select(
            "Choose an option:",
            choices=[
                "Run Lua Code",
                "GPIO Button Test",
                "GPIO LED Test",
                "LCD Display Test",
                "Enter Command Mode",
                "Show Boot Log",
                "Run Games",
                "Love2D Examples",
                "Love2D Games",
                "Simulation Mode (No Hardware)",
                "Exit"
            ]
        ).ask()

        if choice == "Run Lua Code":
            run_lua_interactive(ser)
        elif choice == "GPIO Button Test":
            run_gpio_test(ser)
        elif choice == "GPIO LED Test":
            run_gpio_led_test(ser)
        elif choice == "LCD Display Test":
            run_lcd_test(ser)
        elif choice == "Enter Command Mode":
            enter_command_mode(ser)
        elif choice == "Show Boot Log":
            if show_boot_log(ser):
                break  # Connection closed, exit loop
        elif choice == "Run Games":
            run_games_menu(ser)
        elif choice == "Love2D Examples":
            run_love2d_examples(ser)
        elif choice == "Love2D Games":
            run_love2d_games(ser)
        elif choice == "Simulation Mode (No Hardware)":
            run_simulation_mode()
        elif choice == "Exit":
            break

    ser.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()