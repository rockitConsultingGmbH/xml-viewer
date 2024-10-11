from PyQt5.QtWidgets import QApplication, QLineEdit
from common.connection_manager import ConnectionManager
from database.utils import select_from_description

def populate_description_fields(communication_id):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()

    description_types = ['description', 'description1', 'description2', 'description3']
    input_names = ["description_input", "description_1_input", "description_2_input", "description_3_input"]

    for desc_type, input_name in zip(description_types, input_names):
        result = select_from_description(cursor, communication_id, desc_type)
        if result:
            _, _, description_text, _ = result
            set_input_value(input_name, description_text)

    conn.close()

def set_input_value(widget_name, value):
    widget = next((w for w in QApplication.allWidgets() if isinstance(w, QLineEdit) and w.objectName() == widget_name), None)
    if widget:
        widget.blockSignals(True)
        widget.setText(value or "")
        widget.blockSignals(False)