def load_stylesheet(widget, filepath):
    """Load the stylesheet from a file and apply it to the given widget."""
    try:
        with open(filepath, 'r') as file:
            stylesheet = file.read()
            widget.setStyleSheet(stylesheet)
            print(f"Successfully loaded stylesheet from: {filepath}")
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")
