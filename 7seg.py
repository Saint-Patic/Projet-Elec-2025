from machine import Pin, Timer

# Pins for binary output to the decoder (3, 4, 5, 6)
binary_pins = [3, 4, 5, 6]
gpio_pins = [Pin(i, Pin.OUT) for i in binary_pins]

# Pins for display selection (transistors)
display_select_pins = [Pin(i, Pin.OUT) for i in range(0, 3)]  # GPIO 0, 1, 2

# Global variables
CURRENT_DIGIT = 0
NUMBER_OF_DIGITS = 3
digits = [1, 2, 3]


def digits_to_binary(value):
    """
    Convert a value (0-9) to its binary representation as a list of bits.
    """
    # Ensure value is within 4-bit range (0-15)
    value = value & 0xF  # Mask to 4-bit
    # Return the binary representation as a list of bits
    return [(value >> i) & 1 for i in range(4)][::-1]


def send_binary_to_decoder(value):
    """
    Send a binary representation of the value (0-9) to the decoder via pins 3, 4, 5, 6.
    """
    global gpio_pins
    # Get binary representation using digits_to_binary
    binary_representation = digits_to_binary(value)
    print(f"Sending binary {binary_representation} to decoder for value {value}")
    # Write each bit to the corresponding pin
    for i, pin in enumerate(gpio_pins):
        # Set the pin to the corresponding bit value (0 or 1)
        pin.value(binary_representation[i])


def select_display(value):
    """
    Activate the appropriate display by setting the corresponding transistor pins.
    """
    global display_select_pins
    # Ensure value is within 3-bit range
    value = value & 0xFF  # Mask to 3-bit
    # Write each bit to the corresponding pin
    for i in range(NUMBER_OF_DIGITS):
        display_select_pins[i].value((value >> i) & 1)


def write_displays(timer):
    """
    Update the displays by sending the current digit to the decoder
    and activating the corresponding display.
    """
    global CURRENT_DIGIT, digits, NUMBER_OF_DIGITS

    # Disable all displays first
    select_display(0)
    # Send the current digit to the decoder
    send_binary_to_decoder(digits[CURRENT_DIGIT])
    # Enable the current display
    select_display(1 << CURRENT_DIGIT)
    # Move to the next digit
    CURRENT_DIGIT += 1
    if CURRENT_DIGIT == NUMBER_OF_DIGITS:
        CURRENT_DIGIT = 0
