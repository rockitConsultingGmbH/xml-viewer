from PyQt5.QtWidgets import QApplication, QLineEdit, QCheckBox
from database.xml_data_to_db import get_db_connection

def data_populating(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Communication table
    cursor.execute(
        """SELECT isToPoll, description, description1, description2, description3,
                  pollUntilFound, noTransfer, befoerderungAb, befoerderungBis,
                  pollInterval, watcherEscalationTimeout, preunzip, postzip,
                  renameWithTimestamp, gueltigAb, gueltigBis, findPattern, quitPattern,
                  ackPattern, zipPattern, movPattern, putPattern, rcvPattern
           FROM Communication WHERE name = ?""",
        (name,))
    result = cursor.fetchone()  # Getting data from the Communication table

    if result:
        (is_to_poll, description, description1, description2, description3,
         poll_until_found, no_transfer, befoerderung_ab, befoerderung_bis,
         poll_interval, escalation_timeout, pre_unzip, post_zip, rename_with_timestamp,
         gueltig_ab, gueltig_bis, find_pattern, quit_pattern, ack_pattern, zip_pattern,
         mov_pattern, put_pattern, rcv_pattern) = result

        # Updating the name field in the interface
        name_input = next((widget for widget in QApplication.allWidgets() if
                           isinstance(widget, QLineEdit) and widget.objectName() == "name_input"), None)
        if name_input:
            name_input.blockSignals(True)
            name_input.setText(name)
            name_input.blockSignals(False)

        # Updating the Polling enabled checkbox in the interface
        checkbox = next((widget for widget in QApplication.allWidgets() if
                         isinstance(widget, QCheckBox) and widget.objectName() == "polling_activate_checkbox"), None)
        if checkbox:
            checkbox.blockSignals(True)
            checkbox.setChecked(is_to_poll in [1, '1', True, 'true'])
            checkbox.blockSignals(False)

        # Updating the description inputs in the interface
        description_input = next((widget for widget in QApplication.allWidgets() if
                                  isinstance(widget, QLineEdit) and widget.objectName() == "description_input"), None)
        if description_input:
            description_input.blockSignals(True)
            description_input.setText(description)
            description_input.blockSignals(False)

        for i, desc in enumerate([description1, description2, description3], start=1):
            desc_input = next((widget for widget in QApplication.allWidgets() if
                               isinstance(widget, QLineEdit) and widget.objectName() == f"description_{i}_input"), None)
            if desc_input:
                desc_input.blockSignals(True)
                desc_input.setText(desc)
                desc_input.blockSignals(False)

        # Updating checkboxes for "Poll until found" and "No transfer"
        poll_until_found_checkbox = next((widget for widget in QApplication.allWidgets() if
                                          isinstance(widget,
                                                     QCheckBox) and widget.objectName() == "poll_until_found_checkbox"),
                                         None)
        if poll_until_found_checkbox:
            poll_until_found_checkbox.blockSignals(True)
            poll_until_found_checkbox.setChecked(poll_until_found in [1, '1', True, 'true'])
            poll_until_found_checkbox.blockSignals(False)

        no_transfer_checkbox = next((widget for widget in QApplication.allWidgets() if
                                     isinstance(widget, QCheckBox) and widget.objectName() == "no_transfer_checkbox"),
                                    None)
        if no_transfer_checkbox:
            no_transfer_checkbox.blockSignals(True)
            no_transfer_checkbox.setChecked(no_transfer in [1, '1', True, 'true'])
            no_transfer_checkbox.blockSignals(False)

        # Updating inputs for "Beförderung ab", "Poll Intervall", "Beförderung bis", "Escalation timeout"
        befoerderung_ab_input = next((widget for widget in QApplication.allWidgets() if
                                      isinstance(widget, QLineEdit) and widget.objectName() == "befoerderung_ab_input"),
                                     None)
        if befoerderung_ab_input:
            befoerderung_ab_input.blockSignals(True)
            befoerderung_ab_input.setText(befoerderung_ab)
            befoerderung_ab_input.blockSignals(False)

        befoerderung_bis_input = next((widget for widget in QApplication.allWidgets() if
                                       isinstance(widget,
                                                  QLineEdit) and widget.objectName() == "befoerderung_bis_input"), None)
        if befoerderung_bis_input:
            befoerderung_bis_input.blockSignals(True)
            befoerderung_bis_input.setText(befoerderung_bis)
            befoerderung_bis_input.blockSignals(False)

        poll_interval_input = next((widget for widget in QApplication.allWidgets() if
                                    isinstance(widget, QLineEdit) and widget.objectName() == "poll_interval_input"),
                                   None)
        if poll_interval_input:
            poll_interval_input.blockSignals(True)
            poll_interval_input.setText(poll_interval)
            poll_interval_input.blockSignals(False)

        escalation_timeout_input = next((widget for widget in QApplication.allWidgets() if
                                         isinstance(widget,
                                                    QLineEdit) and widget.objectName() == "escalation_timeout_input"),
                                        None)
        if escalation_timeout_input:
            escalation_timeout_input.blockSignals(True)
            escalation_timeout_input.setText(escalation_timeout)
            escalation_timeout_input.blockSignals(False)

        # Updating checkboxes for "Pre-Unzip", "Post-Zip", and "Rename with Timestamp"
        pre_unzip_checkbox = next((widget for widget in QApplication.allWidgets() if
                                   isinstance(widget, QCheckBox) and widget.objectName() == "pre_unzip_checkbox"), None)
        if pre_unzip_checkbox:
            pre_unzip_checkbox.blockSignals(True)
            pre_unzip_checkbox.setChecked(pre_unzip in [1, '1', True, 'true'])
            pre_unzip_checkbox.blockSignals(False)

        post_zip_checkbox = next((widget for widget in QApplication.allWidgets() if
                                  isinstance(widget, QCheckBox) and widget.objectName() == "post_zip_checkbox"), None)
        if post_zip_checkbox:
            post_zip_checkbox.blockSignals(True)
            post_zip_checkbox.setChecked(post_zip in [1, '1', True, 'true'])
            post_zip_checkbox.blockSignals(False)

        rename_with_timestamp_checkbox = next((widget for widget in QApplication.allWidgets() if
                                               isinstance(widget,
                                                          QCheckBox) and widget.objectName() == "rename_with_timestamp_checkbox"),
                                              None)
        if rename_with_timestamp_checkbox:
            rename_with_timestamp_checkbox.blockSignals(True)
            rename_with_timestamp_checkbox.setChecked(rename_with_timestamp in [1, '1', True, 'true'])
            rename_with_timestamp_checkbox.blockSignals(False)

        # Updating inputs for "Gültig ab" and "Gültig bis"
        gueltig_ab_input = next((widget for widget in QApplication.allWidgets() if
                                 isinstance(widget, QLineEdit) and widget.objectName() == "gueltig_ab_input"), None)
        if gueltig_ab_input:
            gueltig_ab_input.blockSignals(True)
            gueltig_ab_input.setText(gueltig_ab)
            gueltig_ab_input.blockSignals(False)

        gueltig_bis_input = next((widget for widget in QApplication.allWidgets() if
                                  isinstance(widget, QLineEdit) and widget.objectName() == "gueltig_bis_input"), None)
        if gueltig_bis_input:
            gueltig_bis_input.blockSignals(True)
            gueltig_bis_input.setText(gueltig_bis)
            gueltig_bis_input.blockSignals(False)

        # Updating inputs for "findPattern", "quitPattern", "ackPattern", "zipPattern", "movPattern", "putPattern", and "rcvPattern"
        patterns = {
            "find_pattern_input": find_pattern,
            "quit_pattern_input": quit_pattern,
            "ack_pattern_input": ack_pattern,
            "zip_pattern_input": zip_pattern,
            "mov_pattern_input": mov_pattern,
            "put_pattern_input": put_pattern,
            "rcv_pattern_input": rcv_pattern
        }

        for pattern_object_name, pattern_value in patterns.items():
            pattern_input = next((widget for widget in QApplication.allWidgets() if
                                  isinstance(widget, QLineEdit) and widget.objectName() == pattern_object_name), None)
            if pattern_input:
                pattern_input.blockSignals(True)
                pattern_input.setText(pattern_value)
                pattern_input.blockSignals(False)

        # Location table
        cursor.execute(
            "SELECT location, userid, password FROM Location WHERE communication_id = (SELECT id FROM Communication WHERE name = ?) AND locationType = 'sourceLocation'",
            (name,))
        source_result = cursor.fetchall()  # Getting data from the Location table

        # Updating the Source input in the interface
        source_input = next((widget for widget in QApplication.allWidgets() if
                             isinstance(widget, QLineEdit) and widget.objectName() == "source_input"), None)
        if source_input:
            source_input.blockSignals(True)
            source_input.setText(", ".join(location[0] for location in source_result))
            source_input.blockSignals(False)

        # Updating the UserID and Password inputs in the interface
        for location in source_result:
            userid = location[1]
            password = location[2]

            # Update the UserID input
            userid_input = next((widget for widget in QApplication.allWidgets() if
                                 isinstance(widget, QLineEdit) and widget.objectName() == "userid_source_input"), None)
            if userid_input:
                userid_input.blockSignals(True)
                userid_input.setText(userid)
                userid_input.blockSignals(False)

            # Updating the Password input
            password_input = next((widget for widget in QApplication.allWidgets() if
                                   isinstance(widget, QLineEdit) and widget.objectName() == "password_source_input"), None)
            if password_input:
                password_input.blockSignals(True)
                password_input.setText(password)
                password_input.blockSignals(False)

            cursor.execute(
                "SELECT location, userid, password FROM Location WHERE communication_id = (SELECT id FROM Communication WHERE name = ?) AND locationType = 'targetLocation'",
                (name,))
            target_result = cursor.fetchall()

            # Лог для диагностики
            print(f"Target result for '{name}':", target_result)

            # Обновление Target inputs
            target_count = len(target_result)  # Количество записей для targetLocation
            for i in range(target_count):
                if i < 5:  # Если количество записей больше 5, не обрабатываем их
                    location, userid, password = target_result[i]

                    # Обновление полей для Target
                    target_input = next((widget for widget in QApplication.allWidgets() if
                                         isinstance(widget,
                                                    QLineEdit) and widget.objectName() == f"target_{i + 1}_input"),
                                        None)
                    if target_input:
                        target_input.blockSignals(True)
                        target_input.setText(location)
                        target_input.blockSignals(False)

                    # Обновление UserID для Target
                    userid_target_input = next((widget for widget in QApplication.allWidgets() if
                                                isinstance(widget,
                                                           QLineEdit) and widget.objectName() == f"userid_target_{i + 1}_input"),
                                               None)
                    if userid_target_input:
                        userid_target_input.blockSignals(True)
                        userid_target_input.setText(userid)
                        userid_target_input.blockSignals(False)

                    # Обновление Password для Target
                    password_target_input = next((widget for widget in QApplication.allWidgets() if
                                                  isinstance(widget,
                                                             QLineEdit) and widget.objectName() == f"password_target_{i + 1}_input"),
                                                 None)
                    if password_target_input:
                        password_target_input.blockSignals(True)
                        password_target_input.setText(password)
                        password_target_input.blockSignals(False)

            # Очистка полей, если записей меньше 5
            for i in range(5):
                if i >= target_count:
                    target_input = next((widget for widget in QApplication.allWidgets() if
                                         isinstance(widget,
                                                    QLineEdit) and widget.objectName() == f"target_{i + 1}_input"),
                                        None)
                    if target_input:
                        target_input.blockSignals(True)
                        target_input.clear()
                        target_input.blockSignals(False)

                    userid_target_input = next((widget for widget in QApplication.allWidgets() if
                                                isinstance(widget,
                                                           QLineEdit) and widget.objectName() == f"userid_target_{i + 1}_input"),
                                               None)
                    if userid_target_input:
                        userid_target_input.blockSignals(True)
                        userid_target_input.clear()
                        userid_target_input.blockSignals(False)

                    password_target_input = next((widget for widget in QApplication.allWidgets() if
                                                  isinstance(widget,
                                                             QLineEdit) and widget.objectName() == f"password_target_{i + 1}_input"),
                                                 None)
                    if password_target_input:
                        password_target_input.blockSignals(True)
                        password_target_input.clear()
                        password_target_input.blockSignals(False)