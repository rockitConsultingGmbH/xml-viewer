def toggle_inputs(labels, inputs):
    for label, input_field in zip(labels, inputs):
        if label.isVisible():
            label.hide()
            input_field.hide()
        else:
            label.show()
            input_field.show()