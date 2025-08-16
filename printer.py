# -*- coding: utf-8 -*-

"""
Module for handling the printing logic.

This module contains the necessary functions to connect to a network printer
and send commands in the Fingerprint programming language to print a series
of labels.

Disclaimer: The Fingerprint commands used in this module are based on the
specific requirements of the project and have not been verified against an
official command reference, as one could not be located. The code is structured
to be clear and easily modifiable if adjustments to the commands are needed.
"""

import socket

# Define the printer's network address.
# IMPORTANT: This should be changed to the actual IP address of the printer.
PRINTER_IP = "192.168.1.193"
PRINTER_PORT = 9100

def print_labels(n):
    """
    Connects to the printer and sends the commands to print N labels.

    This function establishes a socket connection to the printer, sends the
    initial configuration commands, and then loops N times to print a label
    with a number from 1 to N.

    Args:
        n (int): The number of labels to print.

    Returns:
        tuple: A tuple containing a boolean indicating success and a message.
               (True, "Successfully printed N labels.")
               (False, "Error message.")
    """
    try:
        # --- Start of Fingerprint Command Block ---

        # Initial printer setup.
        # These commands configure the printer's operational parameters.
        # We are assuming these commands are sent once per print job.
        setup_commands = [
            'SET "PRINT METHOD" "DIRECT THERMAL"',  # Use Direct Thermal printing.
            'SET "MEDIA TYPE" "GAP"',              # Use gapped labels.
            'SET "MEDIA WIDTH" 840',               # Set media width in dots.
            'SET "MEDIA LENGTH" 251',              # Set media length in dots.
        ]

        # Start a new print job. In many printer languages, this is done with
        # a command like "PRINT" or by enclosing commands in a specific block.
        # We will assume each label is a separate print job for simplicity.
        # The core of the printing logic will be a loop.

        print_commands = []
        for i in range(1, n + 1):
            # For each label, we generate a block of commands.
            # We will use a scalable font and center the text.
            # The 'Swiss 721' font is a common scalable font on many printers.
            # We use MAGNIFY and JUSTIFY to make the text large and centered.
            label_commands = [
                'FONT "Swiss 721"',           # Select a scalable font.
                'MAGNIFY 10, 10',             # Magnify the font. We guess some values.
                'JUSTIFY CENTER',             # Center the text horizontally.
                f'TEXT "{i}"',                # The text to print (the number).
                'PRINT',                      # The command to print the label.
                'FORMFEED'                    # Eject the label.
            ]
            print_commands.extend(label_commands)

        # Combine all commands into a single string, separated by newlines.
        # The printer will execute these commands sequentially.
        # We add a final newline to ensure the last command is processed.
        full_command_string = "\n".join(setup_commands + print_commands) + "\n"

        # --- End of Fingerprint Command Block ---

        # Open a socket connection to the printer.
        # The 'with' statement ensures the socket is automatically closed.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a timeout for the connection attempt.
            s.settimeout(5)
            s.connect((PRINTER_IP, PRINTER_PORT))

            # Send the command string to the printer.
            # The string must be encoded to bytes, typically in UTF-8.
            s.sendall(full_command_string.encode('utf-8'))

        # If we reach here, the commands were sent successfully.
        return (True, f"Successfully sent print job for {n} labels.")

    except socket.timeout:
        # This error occurs if the printer is not reachable at the given IP/port.
        return (False, f"Connection timed out. Check printer IP ({PRINTER_IP}) and network.")
    except socket.error as e:
        # This handles other network-related errors.
        return (False, f"Socket error: {e}")
    except Exception as e:
        # Catch any other unexpected errors.
        return (False, f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # This block allows for direct testing of the printer module.
    # To use it, run 'python printer.py' from the terminal.
    print("--- Testing printer module ---")

    # Test case: Print 3 labels.
    number_of_labels = 3
    print(f"Attempting to print {number_of_labels} labels to {PRINTER_IP}:{PRINTER_PORT}...")

    success, message = print_labels(number_of_labels)

    if success:
        print(f"SUCCESS: {message}")
    else:
        print(f"ERROR: {message}")

    print("--- Test complete ---")
