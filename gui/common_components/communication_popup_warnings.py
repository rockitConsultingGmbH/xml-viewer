from PyQt5.QtWidgets import QMessageBox


def show_unsaved_changes_warning(main_window):
    reply = QMessageBox.question(main_window, "Unsaved changes",
                                 "If you continue, all unsaved data will be lost. Do you really want to continue?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    return reply


def show_save_error(main_window):
    QMessageBox.warning(main_window, "Warning", "Please fill the name field.", QMessageBox.Ok)
