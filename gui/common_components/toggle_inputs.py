def toggle_inputs(labels, inputs, checkboxes=None):
    if checkboxes is None:
        checkboxes = []
    for label in labels:
        label.setVisible(not label.isVisible())
    for input_field in inputs:
        input_field.setVisible(not input_field.isVisible())
    for checkbox in checkboxes:
        checkbox.setVisible(not checkbox.isVisible())