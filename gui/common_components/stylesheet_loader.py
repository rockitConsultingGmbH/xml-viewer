import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def load_stylesheet(widget, relative_filepath):
    # Get the absolute path of the main script's directory (app.py)
    main_script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    logging.debug(f"Main script directory: {main_script_path}")
    
    # Join the base path with the relative path to create the full path
    filepath = os.path.join(main_script_path, relative_filepath)
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
