import os
from lxml import etree
from utils.export_db_to_xml import db_to_xml_map
from common.connection_manager import ConnectionManager

# DB file path
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_name = os.path.basename(db_path)

def get_columns_from_table(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return columns

def get_rows_from_db_table(cursor, table_name, columns, whereClause="", fetchAll=True):
    columns_str = ", ".join(columns)
    query = f"SELECT {columns_str} FROM {table_name} {whereClause}"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def get_row_from_db_table(cursor, table_name, columns, whereClause=""):
    columns_str = ", ".join(columns)
    query = f"SELECT {columns_str} FROM {table_name} {whereClause}"
    cursor.execute(query)
    row = cursor.fetchone()
    return row

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# Save XML to file
def save_xml_to_file(pretty_xml_as_string, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml_as_string)

# Main function to execute the conversion
def create_xml_from_dbconfig(config_id):
    # Connect to the database
    conn_manager = ConnectionManager()
    conn = conn_manager.get_db_connection() 
    cursor = conn.cursor()

    # Create the root XML element
    root = etree.Element('acs')

    # BasicConfig
    columns = get_columns_from_table(cursor, 'BasicConfig')
    row = get_row_from_db_table(cursor, 'BasicConfig', columns, f"WHERE id = {config_id}")
    basicConfig_id = row['id']
    xml_tree, acsfiletransfer = db_to_xml_map.create_xml_from_basic_config(root, row, columns)

    # LzbConfig
    columns = get_columns_from_table(cursor, 'LzbConfig')
    row = get_row_from_db_table(cursor, 'LzbConfig', columns, f"WHERE basicConfig_id = {basicConfig_id}")
    xml_tree, lzb = db_to_xml_map.create_xml_from_basic_lzb(acsfiletransfer, row)

    # MqConfig
    columns = get_columns_from_table(cursor, 'MqConfig')
    row = get_row_from_db_table(cursor, 'MqConfig', columns, f"WHERE basicConfig_id = {basicConfig_id}")
    mqConfig_id = row['id']
    xml_tree, mqconfig = db_to_xml_map.create_xml_from_mqconfig(acsfiletransfer, row, columns)

    # MqTrigger
    columns = get_columns_from_table(cursor, 'MqTrigger')
    row = get_row_from_db_table(cursor, 'MqTrigger', columns, f"WHERE mqConfig_id = {mqConfig_id}")
    xml_tree = db_to_xml_map.create_xml_from_mqtrigger(mqconfig, row)

    # IPQueue
    columns = get_columns_from_table(cursor, 'IPQueue')
    rows = get_rows_from_db_table(cursor, 'IPQueue', columns, f"WHERE mqConfig_id = {mqConfig_id}")
    for row in rows:
        xml_tree = db_to_xml_map.create_xml_from_ipqueue(mqconfig, row)

    # Communications
    columns = get_columns_from_table(cursor, 'Communication')
    communicationRows = get_rows_from_db_table(cursor, 'Communication', columns, f"WHERE basicConfig_id = {basicConfig_id}")
    for communicationRow in communicationRows:
        communication_id = communicationRow['id']
        communication = etree.SubElement(acsfiletransfer, 'communication')

        # Description
        columns = get_columns_from_table(cursor, 'Description')
        rows = get_rows_from_db_table(cursor, 'Description', columns, f"WHERE communication_id = {communication_id}")
        for row in rows:
            xml_tree = db_to_xml_map.create_xml_from_description(communication, row)

        # Communication
        xml_tree = db_to_xml_map.create_xml_from_communication(communication, communicationRow)

        # Location
        columns = get_columns_from_table(cursor, 'Location')
        rows = get_rows_from_db_table(cursor, 'Location', columns, f"WHERE communication_id = {communication_id}")
        for row in rows:
            xml_tree = db_to_xml_map.create_xml_from_location(communication, row, columns)

        # Command
        columns = get_columns_from_table(cursor, 'Command')
        rows = get_rows_from_db_table(cursor, 'Command', columns, f"WHERE communication_id = {communication_id}")
        for row in rows:
            xml_tree, command = db_to_xml_map.create_xml_from_command(communication, row)
            command_id = row['id']
            # CommandParam
            columns = get_columns_from_table(cursor, 'CommandParam')
            rows = get_rows_from_db_table(cursor, 'CommandParam', columns, f"WHERE command_id = {command_id}")
            for row in rows:
                xml_tree, commandparam = db_to_xml_map.create_xml_from_commandparam(command, row)

    # NameList
    columns = get_columns_from_table(cursor, 'NameList')
    rows = get_rows_from_db_table(cursor, 'NameList', columns, f"WHERE basicConfig_id = {basicConfig_id}")
    for row in rows:
        xml_tree, namelist = db_to_xml_map.create_xml_from_namelist(acsfiletransfer, row)
        nameList_id = row['id']
        # AlternateName
        columns = get_columns_from_table(cursor, 'AlternateName')
        rows = get_rows_from_db_table(cursor, 'AlternateName', columns, f"WHERE nameList_id = {nameList_id}")
        for row in rows:
            xml_tree, entry = db_to_xml_map.create_xml_from_alternatename(namelist, row)

    xml_tree.indent(root, space="    ")
    pretty_xml_tree = xml_tree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
    conn.close()
    return pretty_xml_tree

def export_to_xml(file_path, config_id):
    try:
        pretty_xml_tree = create_xml_from_dbconfig(config_id)
        save_xml_to_file(pretty_xml_tree, file_path)
        print(f"Data has been written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
