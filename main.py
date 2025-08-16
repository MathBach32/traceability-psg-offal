# -*- coding: utf-8 -*-

"""
Main application file for the N-Label Printer.

This file creates the graphical user interface (GUI) using Tkinter.
The user can enter a number (N) and click a button to print N labels.
The application is designed to be in French, using the gettext library
for easy translation.
"""

import tkinter as tk
from tkinter import ttk
import gettext
import os

# Import the printing function from our printer module.
from printer import print_labels

# --- Internationalization (i18n) Setup ---
# This section configures the gettext library to find our French translations.

# The domain 'messages' should match the name of our .mo file.
APP_NAME = "messages"
# The LOCALE_DIR should point to the directory where the 'locale' folder is.
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

# Set up gettext
# This tells gettext where to find the translation files.
# It will look for ./locale/fr/LC_MESSAGES/fr.mo
try:
    fr_translation = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['fr'])
    fr_translation.install()
    _ = fr_translation.gettext
except FileNotFoundError:
    # Fallback to a dummy function if translation file is not found.
    # This way, the app will still run, but in English (the source language).
    print("Translation file not found. Running in default language.")
    _ = lambda s: s


class Application(tk.Frame):
    """
    The main application class for our GUI.

    This class inherits from tk.Frame and holds all our widgets.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title(_("Label Printer"))
        self.master.resizable(False, False) # Make window not resizable
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all the widgets in the window."""

        # --- Input Section ---
        # A label and an entry field for the user to type the number of labels.
        self.input_label = ttk.Label(self, text=_("Number of labels to print:"))
        self.input_label.pack(pady=(0, 5))

        # The Entry widget is where the user types the number.
        self.number_entry = ttk.Entry(self, width=15, justify='center')
        self.number_entry.pack(pady=(0, 10))
        # Set focus on the entry field so the user can start typing immediately.
        self.number_entry.focus()

        # --- Print Button ---
        # The button that starts the printing process.
        # The 'command' option is set to our printing function.
        self.print_button = ttk.Button(self, text=_("Print"), command=self.start_printing)
        self.print_button.pack(pady=(5, 10))

        # --- Status Label ---
        # A label to provide feedback to the user (e.g., "Printing...", "Done.").
        self.status_label = ttk.Label(self, text=_("Enter a number and click Print."), wraplength=300)
        self.status_label.pack(pady=(10, 0))

    def start_printing(self):
        """
        This method is called when the 'Print' button is clicked.
        It validates the input and calls the printing function.
        """
        # Get the value from the entry field.
        input_value = self.number_entry.get()

        # --- Input Validation ---
        if not input_value.isdigit() or int(input_value) <= 0:
            # If the input is not a positive number, show an error message.
            self.status_label.config(text=_("Error: Please enter a positive whole number."))
            return

        # Convert the input to an integer.
        num_to_print = int(input_value)

        # --- Call the Printing Logic ---
        # Update the status to let the user know something is happening.
        self.status_label.config(text=_("Sending to printer..."))
        # This forces the GUI to update immediately.
        self.master.update()

        # Call the print_labels function from our printer module.
        success, message = print_labels(num_to_print)

        # --- Update Status with Result ---
        # We check the success flag and the message content to display
        # a user-friendly, translated message.
        if success:
            # We can make the success message more specific.
            self.status_label.config(text=_("Successfully sent print job for {} labels.").format(num_to_print))
        else:
            # For errors, we can provide translated, generic messages
            # based on the error type.
            if "Connection timed out" in message:
                self.status_label.config(text=_("Error: Connection timed out. Check printer IP and network."))
            elif "Socket error" in message:
                self.status_label.config(text=_("Error: A network error occurred."))
            else:
                self.status_label.config(text=_("Error: An unexpected error occurred."))


# --- Main execution block ---
if __name__ == "__main__":
    # Create the main window.
    root = tk.Tk()

    # Create an instance of our application.
    app = Application(master=root)

    # Start the GUI event loop.
    # This keeps the window open and responsive to user actions.
    app.mainloop()
