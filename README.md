# N-Label Printer

A simple desktop application to print a given number of labels using a network-connected label printer that understands the Fingerprint command language.

This project is designed as a clear and well-commented example for beginner developers, demonstrating a clean project structure, GUI development with Tkinter, internationalization (i18n) with gettext, and direct network communication with a hardware device.

## Features

*   Simple and clean user interface.
*   Prints a user-defined number (N) of labels, numbered 1 to N.
*   Generates printer-specific commands (Fingerprint language).
*   Connects to the printer over a network socket.
*   User interface is in French (Français), with support for translations.
*   Heavily commented code for educational purposes.

## Project Structure

The project is organized into the following files and directories:

*   `main.py`: The main entry point of the application. It contains the Tkinter GUI code and handles user interactions.
*   `printer.py`: A separate module that contains the logic for generating the Fingerprint commands and sending them to the printer.
*   `locale/`: This directory contains the translation files.
    *   `locale/fr/LC_MESSAGES/`: Contains the files for the French translation.
        *   `messages.po`: The human-readable translation file.
        *   `messages.mo`: The compiled machine-readable translation file used by the application.
*   `README.md`: This file.
*   `LICENSE`: The license file for the project (CC BY-NC-SA 4.0).

## Requirements

To run this application, you will need:

*   **Python 3**: The application is written in Python 3.
*   **Tkinter**: This is the standard GUI library for Python and is usually included with Python installations. If it's not available, you may need to install it separately (e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu).
*   **gettext**: The `gettext` tools are required for the translation functionality. On Debian/Ubuntu, you can install them with `sudo apt-get install gettext`.

## How to Run

1.  **Configure the Printer**: Open the `printer.py` file and change the `PRINTER_IP` and `PRINTER_PORT` variables to match your printer's network address.

2.  **Run the Application**: Open a terminal, navigate to the project's root directory, and run the following command:
    ```bash
    python3 main.py
    ```

3.  **Use the Application**:
    *   Enter the number of labels you wish to print in the input field.
    *   Click the "Imprimer" (Print) button.
    *   The status label at the bottom will show the result of the print job.

## How It Works

### The GUI (`main.py`)

The graphical interface is built using Python's built-in **Tkinter** library. It's a simple window with an input field, a button, and a label to show status messages.

To make the application translatable, all user-visible strings (like "Print" or "Number of labels to print:") are wrapped in a function call like `_("text")`. The **gettext** library is responsible for replacing these strings with their French translations at runtime by looking them up in the `.mo` file.

### The Printing Logic (`printer.py`)

The `print_labels` function in this module does the heavy lifting. When called, it:
1.  Constructs a series of commands in the **Fingerprint** printer language. This includes setting up the printer (media size, print method) and then looping to create the commands for each individual label.
2.  Opens a **network socket** to the printer's IP address and port.
3.  Sends the commands as a byte stream to the printer.
4.  Includes error handling for common network issues, like a timeout if the printer is not available.

The Fingerprint commands are hard-coded based on the project requirements. They are designed to print a centered, magnified number on each label.
