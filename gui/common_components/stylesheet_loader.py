import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def load_stylesheet(widget, relative_filepath):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    filepath = os.path.join(base_path, relative_filepath)
    
    try:
        with open(filepath, 'r') as file:
            stylesheet = file.read()
            widget.setStyleSheet(stylesheet)
            logging.debug(f"Successfully loaded stylesheet from: {filepath}")
    except Exception as e:
        logging.debug(f"Failed to load stylesheet: {e}")
