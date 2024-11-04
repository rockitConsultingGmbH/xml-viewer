import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def load_stylesheet(widget, filepath):
    try:
        with open(filepath, 'r') as file:
            stylesheet = file.read()
            widget.setStyleSheet(stylesheet)
            logging.debug(f"Successfully loaded stylesheet from: {filepath}")
    except Exception as e:
        logging.debug(f"Failed to load stylesheet: {e}")
