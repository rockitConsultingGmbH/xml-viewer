import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def load_stylesheet(widget, relative_filepath):
    # Get the base path using _MEIPASS if it exists (PyInstaller compatibility)
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    filepath = os.path.join(base_path, relative_filepath)
    
    logging.debug(f"Full path to stylesheet: {filepath}")
    
    try:
        with open(filepath, 'r') as file:
            stylesheet = file.read()
            widget.setStyleSheet(stylesheet)
            logging.debug(f"Successfully loaded stylesheet from: {filepath}")
    except FileNotFoundError:
        logging.debug(f"File not found at path: {filepath}")
    except Exception as e:
        logging.debug(f"Failed to load stylesheet: {e}")

# Usage: load_stylesheet(widget, 'css/tree_widget_styling.qss')
