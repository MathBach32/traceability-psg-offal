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

        # 1. Start (once): The setup commands.
        setup_commands = [
            'SETUP "Media,Media Type,Label (w Gaps)"',
            'SETUP "Media,Media Size,Width,840"',
            'SETUP "Print Defs,Print Method,Direct Thermal"',
        ]

        # 2. Middle (in a loop from 1 to N): The printing block.
        print_commands = []
        for i in range(1, n + 1):
            label_commands = [
                "CLL",
                'FONT "IPLFNT34H"',
                "MAGNIFY 2, 2",
                "PRPOS 420, 150",
                "ALIGN 5",
                f'PRTXT "{i}"',
                "PRINTFEED",
            ]
            print_commands.extend(label_commands)

        # 3. End (once): The cleanup command.
        end_command = ["DEFAULT"]

        # Combine all commands into a single string, separated by newlines.
        # The printer will execute these commands sequentially.
        # We add a final newline to ensure the last command is processed.
        all_commands = setup_commands + print_commands + end_command
        full_command_string = "\n".join(all_commands) + "\n"

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
